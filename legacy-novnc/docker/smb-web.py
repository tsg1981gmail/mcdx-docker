#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mdcx-diy 挂载管理服务（宿主机，仅放行 docker 网桥/本机来源，对外经容器 nginx /manager/ 登录访问）
支持两类：
  - SMB 局域网共享：mount.cifs -> /vol1/smb/<名称>，容器内 /media/<名称>
  - 宿主机文件夹：mount --bind -> /vol1/smb/<名称>，容器内 /media/<名称>
纯标准库实现。
"""
import ipaddress
import json
import os
import re
import subprocess
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE = os.environ.get("MDCX_SMB_BASE", "/vol1/smb")
HOST, PORT = "0.0.0.0", 33344
ALLOWED_NETS = [ipaddress.ip_network("127.0.0.0/8"), ipaddress.ip_network("172.16.0.0/12")]
NAME_RE = re.compile(r"^[\w\u4e00-\u9fa5][\w\u4e00-\u9fa5 ._-]{0,63}$")
SOURCE_RE = re.compile(r"^//[^/\s]+/[^\s]+$")
CREDS_DIR = "/etc/mdcx-smb-creds"

PAGE = r"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<title>挂载管理</title>
<style>
 body{font-family:system-ui,"PingFang SC","Microsoft YaHei",sans-serif;background:#f5f6f8;margin:0;color:#222}
 .wrap{max-width:780px;margin:24px auto;padding:0 16px}
 h1{font-size:20px}
 .card{background:#fff;border:1px solid #e3e5e8;border-radius:10px;padding:18px;margin-top:16px}
 .tabs{display:flex;gap:8px;margin-top:16px}
 .tab{padding:8px 18px;border:1px solid #c9cdd3;border-radius:8px;cursor:pointer;background:#fff;font-size:14px}
 .tab.on{background:#2b6cb0;color:#fff;border-color:#2b6cb0}
 .panel{display:none}
 .panel.on{display:block}
 label{display:block;font-size:13px;margin:10px 0 4px}
 input{width:100%;box-sizing:border-box;padding:8px 10px;border:1px solid #c9cdd3;border-radius:6px;font-size:14px}
 .row{display:flex;gap:10px} .row>div{flex:1}
 button{margin-top:14px;background:#2b6cb0;color:#fff;border:0;padding:10px 22px;border-radius:6px;font-size:14px;cursor:pointer}
 button:hover{background:#245a94}
 button[disabled]{opacity:.5}
 .ok{color:#1a7f37}.err{color:#c0392b}
 table{width:100%;border-collapse:collapse;font-size:14px}
 th,td{text-align:left;padding:8px;border-bottom:1px solid #eee}
 .btn-m{font-size:12px;padding:4px 12px;margin:0}
 code{background:#eef1f4;padding:2px 6px;border-radius:4px}
 .hint{font-size:12px;color:#666}
 #msg{padding:10px 14px;border-radius:6px;display:none;margin-top:12px}
</style>
</head>
<body>
<div class="wrap">
 <h1>挂载管理</h1>
 <p class="hint">挂载后自动出现在 mdcx-diy 容器 <code>/media/&lt;名称&gt;</code>，在网页应用里直接选该路径即可，无需重启容器。</p>
 <div class="tabs">
   <div class="tab on" data-t="smb">SMB 局域网共享</div>
   <div class="tab" data-t="host">宿主机文件夹</div>
 </div>
 <div class="card panel on" id="p-smb">
  <form id="mSMB">
   <div class="row">
    <div><label>名称（容器内 /media/ 下的目录名）</label><input id="s_name" placeholder="如 movies" required></div>
    <div><label>SMB 地址</label><input id="s_source" placeholder="//192.168.1.5/Movies" required></div>
   </div>
   <div class="row">
    <div><label>用户名</label><input id="s_user"></div>
    <div><label>密码</label><input id="s_pass" type="password"></div>
   </div>
   <div class="row">
    <div><label>SMB 版本（老设备可试 2.0 / 1.0）</label><input id="s_vers" value="3.0" placeholder="3.0"></div>
    <div><label><input type="checkbox" id="s_persist" style="width:auto"> 开机自动挂载</label></div>
   </div>
   <button type="submit">挂载</button>
  </form>
 </div>
 <div class="card panel" id="p-host">
  <form id="mHost">
   <div class="row">
    <div><label>名称（容器内 /media/ 下的目录名）</label><input id="h_name" placeholder="如 video" required></div>
    <div><label>宿主机文件夹（绝对路径）</label><input id="h_path" placeholder="/vol1/1000/video" required></div>
   </div>
   <div class="row">
    <div><label>只读（源库建议勾选，防止误删）</label><input type="checkbox" id="h_ro" style="width:auto"></div>
    <div><label><input type="checkbox" id="h_persist" style="width:auto"> 开机自动挂载（写入 /etc/fstab）</label></div>
   </div>
   <button type="submit">挂载</button>
  </form>
 </div>
 <div id="msg"></div>
 <div class="card">
  <h2 style="font-size:16px">已挂载</h2>
  <table><thead><tr><th>名称</th><th>来源</th><th>容器内路径</th><th></th></tr></thead><tbody id="tbody"></tbody></table>
 </div>
</div>
<script>
const $=id=>document.getElementById(id);
document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>{
  document.querySelectorAll(".tab").forEach(x=>x.classList.remove("on"));
  document.querySelectorAll(".panel").forEach(x=>x.classList.remove("on"));
  t.classList.add("on");$("p-"+t.dataset.t).classList.add("on");
});
function show(msg,ok){const m=$("msg");m.style.display="block";m.className=ok?"ok":"err";m.textContent=msg;}
async function api(path,body){
  const r=await fetch(path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body||{})});
  return r.json();
}
async function load(){
  const d=await (await fetch("api/list")).json();
  const tb=$("tbody");tb.innerHTML="";
  for(const m of d.mounts){
    const tr=document.createElement("tr");
    tr.innerHTML=`<td>${m.name}</td><td><code>${m.source}</code></td><td><code>/media/${m.name}</code></td>`+
      `<td><button class="btn-m" data-name="${m.name}">卸载</button></td>`;
    tr.querySelector("button").onclick=async()=>{
      const r=await api("api/umount",{name:m.name});
      show(r.ok?`已卸载 ${m.name}`:r.error,r.ok);load();
    };
    tb.appendChild(tr);
  }
}
$("mSMB").onsubmit=async(e)=>{
  e.preventDefault();
  const btn=e.target.querySelector("button");btn.disabled=true;
  const r=await api("api/mount",{type:"smb",name:$("s_name").value.trim(),source:$("s_source").value.trim(),
    user:$("s_user").value,pass:$("s_pass").value,vers:$("s_vers").value.trim()||"3.0",persist:$("s_persist").checked});
  show(r.ok?r.message:r.error,r.ok);
  if(r.ok)e.target.reset();
  btn.disabled=false;load();
};
$("mHost").onsubmit=async(e)=>{
  e.preventDefault();
  const btn=e.target.querySelector("button");btn.disabled=true;
  const r=await api("api/mount",{type:"host",name:$("h_name").value.trim(),path:$("h_path").value.trim(),
    ro:$("h_ro").checked,persist:$("h_persist").checked});
  show(r.ok?r.message:r.error,r.ok);
  if(r.ok)e.target.reset();
  btn.disabled=false;load();
};
load();
</script>
</body>
</html>"""


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def list_mounts():
    out = run(["mount"]).stdout
    rows = []
    for line in out.splitlines():
        if BASE not in line:
            continue
        m = re.match(r"(\S+) on (/vol1/smb/[^ ]+) type \S+", line)
        if not m:
            continue
        rows.append({"name": m.group(2).rsplit("/", 1)[1], "source": m.group(1)})
    return rows


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _allowed(self):
        try:
            addr = ipaddress.ip_address(self.client_address[0])
        except ValueError:
            return False
        return any(addr in net for net in ALLOWED_NETS)

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False))

    def do_GET(self):
        if not self._allowed():
            return self._json({"ok": False, "error": "forbidden"}, 403)
        path = urllib.parse.urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._send(200, PAGE, "text/html; charset=utf-8")
        elif path == "/api/list":
            self._json({"ok": True, "mounts": list_mounts()})
        else:
            self._json({"ok": False, "error": "not found"}, 404)

    def do_POST(self):
        if not self._allowed():
            return self._json({"ok": False, "error": "forbidden"}, 403)
        length = int(self.headers.get("Content-Length", 0) or 0)
        try:
            data = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            data = {}
        path = urllib.parse.urlparse(self.path).path
        if path == "/api/mount":
            if data.get("type") == "host":
                self._handle_mount_host(data)
            else:
                self._handle_mount_smb(data)
        elif path == "/api/umount":
            self._handle_umount(data)
        else:
            self._json({"ok": False, "error": "not found"}, 404)

    def _handle_mount_smb(self, data):
        name = str(data.get("name", "")).strip()
        src = str(data.get("source", "")).strip()
        user = str(data.get("user", "")).strip()
        pw = str(data.get("pass", ""))
        vers = str(data.get("vers", "3.0")).strip() or "3.0"
        persist = bool(data.get("persist"))
        if not NAME_RE.match(name):
            return self._json({"ok": False, "error": "名称不合法（不要包含 / 或 ..）"})
        if not SOURCE_RE.match(src):
            return self._json({"ok": False, "error": "地址格式应为 //IP/共享名"})
        if vers not in ("1.0", "2.0", "2.1", "3.0"):
            return self._json({"ok": False, "error": "SMB 版本请填 3.0 / 2.0 / 1.0"})
        target = os.path.join(BASE, name)
        if os.path.ismount(target):
            return self._json({"ok": False, "error": f"{name} 已挂载，请先卸载再重挂"})
        os.makedirs(target, exist_ok=True)
        opts = (
            f"username={user},password={pw},vers={vers},uid=1000,gid=1000,"
            "iocharset=utf8,file_mode=0664,dir_mode=0775,noserverino"
        )
        r = run(["/usr/sbin/mount.cifs", src, target, "-o", opts])
        if r.returncode != 0:
            try:
                os.rmdir(target)
            except OSError:
                pass
            return self._json({"ok": False, "error": r.stderr.strip() or r.stdout.strip() or "挂载失败"})
        if persist:
            ok, err = persist_smb(name, src, vers, user, pw)
            if not ok:
                return self._json({"ok": True, "message": f"挂载成功 → /media/{name}（开机自动挂载写入失败：{err}）"})
        return self._json({"ok": True, "message": f"挂载成功 → 容器内路径 /media/{name}"})

    def _handle_mount_host(self, data):
        name = str(data.get("name", "")).strip()
        path = str(data.get("path", "")).strip()
        ro = bool(data.get("ro"))
        persist = bool(data.get("persist"))
        if not NAME_RE.match(name):
            return self._json({"ok": False, "error": "名称不合法（不要包含 / 或 ..）"})
        real = os.path.realpath(path)
        if not real.startswith("/") or not os.path.isdir(real):
            return self._json({"ok": False, "error": "宿主机路径不存在或不是目录"})
        base_real = os.path.realpath(BASE)
        if real == base_real or real.startswith(base_real + "/"):
            return self._json({"ok": False, "error": "不能挂载挂载区自身或其子目录"})
        target = os.path.join(BASE, name)
        if os.path.ismount(target):
            return self._json({"ok": False, "error": f"{name} 已挂载，请先卸载再重挂"})
        os.makedirs(target, exist_ok=True)
        cmd = ["/usr/bin/mount", "--bind"]
        if ro:
            cmd += ["-o", "ro"]
        cmd += [real, target]
        r = run(cmd)
        if r.returncode != 0:
            try:
                os.rmdir(target)
            except OSError:
                pass
            return self._json({"ok": False, "error": r.stderr.strip() or "挂载失败"})
        if persist:
            ok, err = persist_bind(name, real, ro)
            if not ok:
                return self._json({"ok": True, "message": f"挂载成功 → /media/{name}（开机自动挂载写入失败：{err}）"})
        return self._json({"ok": True, "message": f"挂载成功 → 容器内路径 /media/{name}（{'只读' if ro else '可读写'}）"})

    def _handle_umount(self, data):
        name = str(data.get("name", "")).strip()
        if not NAME_RE.match(name):
            return self._json({"ok": False, "error": "名称不合法"})
        target = os.path.join(BASE, name)
        r = run(["/usr/bin/umount", target])
        if r.returncode != 0 and not os.path.ismount(target):
            return self._json({"ok": True, "message": f"{name} 已清理"})
        if r.returncode != 0:
            return self._json({"ok": False, "error": r.stderr.strip() or "卸载失败"})
        persist_remove(name)
        try:
            os.rmdir(target)
        except OSError:
            pass
        return self._json({"ok": True, "message": f"已卸载 {name}"})


def persist_smb(name, src, vers, user, pw):
    try:
        os.makedirs(CREDS_DIR, exist_ok=True)
        cred = os.path.join(CREDS_DIR, name)
        with open(cred, "w", encoding="utf-8") as f:
            f.write(f"username={user}\npassword={pw}\n")
        os.chmod(cred, 0o600)
        target = os.path.join(BASE, name)
        opts = (
            f"credentials={cred},uid=1000,gid=1000,iocharset=utf8,vers={vers},"
            "file_mode=0664,dir_mode=0775,nofail"
        )
        line = f"{src} {target} cifs {opts} 0 0\n"
        with open("/etc/fstab", "r", encoding="utf-8") as f:
            content = f.read()
        if target not in content:
            with open("/etc/fstab", "a", encoding="utf-8") as f:
                f.write(line)
        return True, ""
    except Exception as e:
        return False, str(e)


def persist_bind(name, src, ro):
    try:
        target = os.path.join(BASE, name)
        opts = "bind,ro,nofail" if ro else "bind,nofail"
        line = f"{src} {target} none {opts} 0 0\n"
        with open("/etc/fstab", "r", encoding="utf-8") as f:
            content = f.read()
        if target not in content:
            with open("/etc/fstab", "a", encoding="utf-8") as f:
                f.write(line)
        return True, ""
    except Exception as e:
        return False, str(e)


def persist_remove(name):
    cred = os.path.join(CREDS_DIR, name)
    target = os.path.join(BASE, name)
    try:
        with open("/etc/fstab", "r", encoding="utf-8") as f:
            lines = [ln for ln in f if target not in ln]
        with open("/etc/fstab", "w", encoding="utf-8") as f:
            f.writelines(lines)
    except OSError:
        pass
    try:
        if os.path.exists(cred):
            os.remove(cred)
    except OSError:
        pass


if __name__ == "__main__":
    srv = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"mdcx-smb-web listening on {HOST}:{PORT}")
    srv.serve_forever()