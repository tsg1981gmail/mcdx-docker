# 原版界面控件清单（来自 mdcx/views/MDCx.ui 自动解析）

> 依据：原版主窗口共 7 个页面；设置页含 60 个 QGroupBox 配置分组。

| 页面 | 控件名 | 类型 | 文本 |
|---|---|---|---|
| 影片刮削 | `pushButton_start_cap` | QPushButton | 开始 |
| 影片刮削 | `label_number1` | QLabel | 番号： |
| 影片刮削 | `label_13` | QLabel | 日期： |
| 影片刮削 | `label_actor1` | QLabel | 演员： |
| 影片刮削 | `label_18` | QLabel | 简介： |
| 影片刮削 | `label_title1` | QLabel | 标题： |
| 影片刮削 | `label_23` | QLabel | 导演： |
| 影片刮削 | `label_24` | QLabel | 发行： |
| 影片刮削 | `label_30` | QLabel | 制作： |
| 影片刮削 | `label_31` | QLabel | 系列： |
| 影片刮削 | `label_33` | QLabel | 标签： |
| 影片刮削 | `checkBox_cover` | QCheckBox | 显示封面 |
| 影片刮削 | `label_result` | QLabel | 等待开始 ... |
| 影片刮削 | `label_22` | QLabel | 时长： |
| 影片刮削 | `label_thumb` | QLabel | 缩略图 |
| 影片刮削 | `label_poster` | QLabel | 封面图 |
| 影片刮削 | `label_poster1` | QLabel | 封面： |
| 影片刮削 | `treeWidget_number` | QTreeWidget |  |
| 影片刮削 | `label_file_path` | QLabel | 视频目录设置：【设置】-【目录】-【待刮削视频目录】。程序将刮削该目录及子目录的所有文件。 |
| 影片刮削 | `pushButton_select_media_folder` | QPushButton | 选择目录 |
| 影片刮削 | `pushButton_play` | QPushButton |  |
| 影片刮削 | `pushButton_open_folder` | QPushButton |  |
| 影片刮削 | `pushButton_open_nfo` | QPushButton |  |
| 影片刮削 | `pushButton_right_menu` | QPushButton |  |
| 影片刮削 | `pushButton_tree_clear` | QPushButton |  |
| 日志 | `textBrowser_log_main_2` | QTextBrowser |  |
| 日志 | `pushButton_start_cap2` | QPushButton | 开始 |
| 日志 | `textBrowser_log_main` | QTextBrowser |  |
| 日志 | `pushButton_show_hide_logs` | QPushButton |  |
| 日志 | `pushButton_view_failed_list` | QPushButton | 失败 0 |
| 日志 | `textBrowser_log_main_3` | QTextBrowser |  |
| 日志 | `pushButton_scraper_failed_list` | QPushButton | 当有失败任务时，点击可以一键刮削当前失败列表 |
| 日志 | `pushButton_save_failed_list` | QPushButton |  |
| 网络检测 | `textBrowser_net_main` | QTextBrowser |  |
| 网络检测 | `pushButton_check_net` | QPushButton | 开始检测 |
| 网络检测 | `pushButton_net_copy` | QPushButton | 复制结果 |
| 网络检测 | `pushButton_net_retry` | QPushButton | 重试失败项 |
| 网络检测 | `pushButton_net_settings` | QPushButton | 打开网络设置 |
| 工具 | `groupBox_7` | QGroupBox | 单文件刮削（指定某个文件的番号网址进行刮削，当存在相同番号时可用这个） |
| 工具 | `pushButton_select_file` | QPushButton | 选择文件 |
| 工具 | `lineEdit_appoint_url` | QLineEdit |  |
| 工具 | `label_10` | QLabel | *番号网址： |
| 工具 | `pushButton_start_single_file` | QPushButton | 刮削 |
| 工具 | `label_3` | QLabel | *文件路径： |
| 工具 | `label` | QLabel | 不要填写网站首页地址！！！要填写该番号的网页地址！！！然后选择对应网站，点击刮削即可！ |
| 工具 | `lineEdit_single_file_path` | QLineEdit |  |
| 工具 | `pushButton_select_file_clear_info` | QPushButton | 清空信息 |
| 工具 | `groupBox_13` | QGroupBox | 裁剪图片（将某个图片裁剪为封面图大小，支持加水印） |
| 工具 | `pushButton_select_thumb` | QPushButton | 选择图片 |
| 工具 | `label_6` | QLabel | 此工具支持拖动选择裁剪范围，可将图片裁剪为封面图（poster）。 |
| 工具 | `groupBox_19` | QGroupBox | 检查演员缺失番号（检查资源库中指定演员本地缺失的番号） |
| 工具 | `lineEdit_actors_name` | QLineEdit |  |
| 工具 | `label_53` | QLabel | 演员名： |
| 工具 | `lineEdit_local_library_path` | QLineEdit |  |
| 工具 | `label_72` | QLabel | 本地资源库： |
| 工具 | `pushButton_find_missing_number` | QPushButton | 检查缺失番号 |
| 工具 | `pushButton_select_local_library` | QPushButton | 选择目录 |
| 工具 | `label_62` | QLabel | 本地资源库和演员名都可以填写多个，以逗号分开（中英文逗号都可以） |
| 工具 | `groupBox_6` | QGroupBox | 移动视频、字幕（将待刮削目录下所有子目录中的视频移动到一个目录中以方便进行查看） |
| 工具 | `pushButton_move_mp4` | QPushButton | 开始移动 |
| 工具 | `label_41` | QLabel | 排除目录： |
| 工具 | `lineEdit_escape_dir_move` | QLineEdit |  |
| 工具 | `label_8` | QLabel | 移动「待刮削视频目录」中的所有视频和字幕到「待刮削视频目录」下的「Movie_moved」目录下。 |
| 工具 | `groupBox_21` | QGroupBox | 软链接助手（将挂载的网盘文件目录及子目录中的所有视频一键创建软链接到本地） |
| 工具 | `lineEdit_localdisk_path` | QLineEdit |  |
| 工具 | `label_338` | QLabel | 本地目录： |
| 工具 | `lineEdit_netdisk_path` | QLineEdit |  |
| 工具 | `label_339` | QLabel | 网盘目录： |
| 工具 | `pushButton_creat_symlink` | QPushButton | 一键创建软链接 |
| 工具 | `pushButton_select_netdisk_path` | QPushButton | 选择目录 |
| 工具 | `label_340` | QLabel | 本地目录中的软链接文件位置将同步按照网盘的文件目录结构创建 |
| 工具 | `pushButton_select_localdisk_path` | QPushButton | 选择目录 |
| 工具 | `checkBox_copy_netdisk_nfo` | QCheckBox | 同时复制网盘目录的nfo、图片、字幕文件到软链接目录 |
| 工具 | `label_341` | QLabel | 勾选后将同时复制网盘中刮削好的nfo等文件到本地，或者你也可以重新刮削这些软链接 |
| 工具 | `checkBox_create_link` | QCheckBox | 刮削过程中自动创建软链接 |
| 工具 | `groupBox_actor_db_maintenance` | QGroupBox | 演员库维护（直接操作 actor_database.xlsx，复用当前配置的 TMDB API） |
| 工具 | `label_actor_db_desc` | QLabel | 以下操作均直接读写 actor_database.xlsx 文件，无需输入演员名单。 |
| 工具 | `pushButton_actor_db_translate` | QPushButton | 补全中文名 |
| 工具 | `pushButton_actor_db_link` | QPushButton | 补全 LibreDMM 链接 |
| 工具 | `label_actor_db_translate_desc` | QLabel | 扫描已有 TMDB ID 缺中文名的条目 |
| 工具 | `label_actor_db_link_desc` | QLabel | 扫描已有 TMDB ID 缺链接的条目 |
| 工具 | `pushButton_actor_db_open` | QPushButton | 打开演员数据库 |
| 工具 | `pushButton_actor_db_stop` | QPushButton | 停止当前维护任务 |
| 工具 | `label_actor_db_open_desc` | QLabel | 用默认程序打开 xlsx 供查看与手工编辑 |
| 工具 | `label_actor_db_note` | QLabel | 提示：补全结果将输出到日志页。所有按钮均防重入，运行中按钮禁用。 |
| 工具 | `pushButton_actor_db_clean_male` | QPushButton | 剔除男演员 |
| 工具 | `pushButton_actor_db_fill_minnano` | QPushButton | minnano 补全 |
| 工具 | `label_actor_db_fill_minnano_desc` | QLabel | 从 minnano-av 补全缺生日/简介，日文字段自动翻译 |
| 工具 | `pushButton_actor_db_verify_tmdbid` | QPushButton | 校验 tmdbid 有效性 |
| 工具 | `label_actor_db_verify_tmdbid_desc` | QLabel | 失效 id 清除后自动按名字重搜补回新 id（搜不到则保持无 id，刮削兜底） |
| 工具 | `pushButton_actor_db_check` | QPushButton | 检查用户库 |
| 工具 | `label_actor_db_check_desc` | QLabel | 检查格式错误、数据异常，安全项自动修复，tmdb 项给人工修复步骤 |
| 工具 | `pushButton_actor_db_fill_zh_javdb` | QPushButton | JavDB 中文名 |
| 工具 | `label_actor_db_fill_zh_javdb_desc` | QLabel | JavDB 的 name_zht 转简体补全中文名；仅处理「中文==日文原名」的行 |
| 工具 | `lineEdit_actor_db_nfo_dir` | QLineEdit | 选择 nfo 目录 |
| 工具 | `pushButton_actor_db_pick_nfo_dir` | QPushButton | 选择目录 |
| 工具 | `pushButton_actor_db_update_nfo_tmdbid` | QPushButton | 更新 nfo tmdbid |
| 工具 | `label_actor_db_update_nfo_desc` | QLabel | 用本地库新 id 覆盖 nfo 旧 id；原本没有的补上（nfo 是持久源，改这里 Emby 重扫才 |
| 工具 | `pushButton_actor_db_sync_aliases` | QPushButton | 补全别名 |
| 工具 | `comboBox_actor_db_alias_source` | QComboBox |  |
| 工具 | `checkBox_actor_db_alias_all` | QCheckBox | 全量更新（并入） |
| 工具 | `label_actor_db_sync_offset` | QLabel | 起始行 |
| 工具 | `spinBox_actor_db_sync_offset` | QSpinBox |  |
| 工具 | `label_actor_db_sync_limit` | QLabel | 限量 |
| 工具 | `spinBox_actor_db_sync_limit` | QSpinBox |  |
| 工具 | `label_actor_db_sync_slice_hint` | QLabel | 0 起始行+5000 限量 = 默认行为 |
| 工具 | `label_actor_db_sync_aliases_desc` | QLabel | 来源 TMDB 需配置 API Key；minnano 直接抓取みんなのAV。默认仅补缺别名的行，勾 |
| 工具 | `groupBox_cover_backfill` | QGroupBox | 封面补图（按番号补齐缺失的封面、缩略图，复用当前配置的各项规则） |
| 工具 | `label_cover_backfill_desc` | QLabel | 输入番号（多个用空格分隔），将自动刮削并补齐封面和缩略图。复用当前配置的站点优先级、命名、裁切、水印 |
| 工具 | `lineEdit_cover_backfill_numbers` | QLineEdit | 例如：SSIS-001 ABF-371 JIMMY-003 |
| 工具 | `pushButton_cover_backfill_start` | QPushButton | 开始补图 |
| 工具 | `checkBox_cover_backfill_overwrite` | QCheckBox | 覆盖已有图片 |
| 工具 | `checkBox_cover_backfill_watermark` | QCheckBox | 添加水印 |
| 工具 | `label_cover_backfill_note` | QLabel | 提示：补图结果将输出到日志页，可在日志页查看详细进度和错误信息。 |
| 工具 | `groupBox_scrape_cache` | QGroupBox | 刮削缓存管理（断点续刮/失败重试状态，清缓存只影响是否跳过，不删已生成 NFO） |
| 工具 | `label_scrape_cache_done` | QLabel | 已完成：0 |
| 工具 | `label_scrape_cache_failed` | QLabel | 失败：0 |
| 工具 | `label_scrape_cache_exhausted` | QLabel | 超限失败：0 |
| 工具 | `label_scrape_cache_total` | QLabel | 总计：0 |
| 工具 | `pushButton_scrape_cache_refresh` | QPushButton | 刷新统计 |
| 工具 | `label_scrape_cache_dbpath` | QLabel | 数据库：未加载 |
| 工具 | `label_scrape_cache_dbsize` | QLabel | 大小：0 KB |
| 工具 | `tableWidget_scrape_cache_failed` | QTableWidget |  |
| 工具 | `pushButton_scrape_cache_export` | QPushButton | 导出失败列表 CSV |
| 工具 | `pushButton_scrape_cache_reset` | QPushButton | 重置选中记录 |
| 工具 | `pushButton_scrape_cache_clear` | QPushButton | 清空全部缓存 |
| 设置 | `tabWidget` | QTabWidget |  |
| 设置 | `groupBox_16` | QGroupBox | 刮削目录 |
| 设置 | `lineEdit_movie_softlink_path` | QLineEdit |  |
| 设置 | `pushButton_select_softlink_folder` | QPushButton | 选择目录 |
| 设置 | `label_58` | QLabel | 指不想要刮削的目录，可以填写多个目录，以逗号分开（中英文逗号都可以） |
| 设置 | `label_49` | QLabel | 待刮削视频目录： |
| 设置 | `lineEdit_escape_dir` | QLineEdit |  |
| 设置 | `checkBox_no_escape_dir` | QCheckBox | 不排除 |
| 设置 | `label_56` | QLabel | 可填一个或多个视频目录，多个目录用英文 ; 或中文 ；分隔。 刮削各目录（含子目录）中的视频元数据。 |
| 设置 | `checkBox_scrape_softlink_path` | QCheckBox | 在以下目录为待刮削目录中的视频创建软链接，然后刮削以下目录（适合网盘用户） |
| 设置 | `label_47` | QLabel | 成功输出目录： |
| 设置 | `lineEdit_movie_path` | QLineEdit |  |
| 设置 | `pushButton_select_media_folder_setting_page` | QPushButton | 选择目录 |
| 设置 | `label_48` | QLabel | 排除目录： |
| 设置 | `label_57` | QLabel | 指刮削失败时，视频将移动到这个文件夹。输出目录可以不在待刮削视频目录下 |
| 设置 | `lineEdit_fail` | QLineEdit |  |
| 设置 | `pushButton_select_failed_folder` | QPushButton | 选择目录 |
| 设置 | `label_46` | QLabel | 失败输出目录： |
| 设置 | `lineEdit_success` | QLineEdit |  |
| 设置 | `pushButton_select_sucess_folder` | QPushButton | 选择目录 |
| 设置 | `label_29` | QLabel | 指刮削成功时，视频将移动到这个文件夹。输出目录可以不在待刮削视频目录下 |
| 设置 | `label_383` | QLabel | <p>如果创建软链接时要复制图片和NFO，请到「工具」-「软链接助手」勾选即可</p><p>1，软链 |
| 设置 | `groupBox_32` | QGroupBox | 文件扫描设置 |
| 设置 | `label_336` | QLabel | 检查软链接： |
| 设置 | `label_337` | QLabel | 勾选后将检查软链接文件指向的目标文件是否存在，若不存在则会删除该软链接 |
| 设置 | `label_348` | QLabel | 支持记录和跳过已刮削成功的文件，避免新增视频时重复刮削之前成功的文件 |
| 设置 | `checkBox_skip_success_file` | QCheckBox | 跳过之前已刮削成功的文件 |
| 设置 | `checkBox_record_success_file` | QCheckBox | 记录刮削成功的文件列表 |
| 设置 | `pushButton_view_success_file` | QPushButton | 查看 |
| 设置 | `lineEdit_escape_size` | QLineEdit |  |
| 设置 | `checkBox_no_escape_file` | QCheckBox | 不跳过 |
| 设置 | `label_346` | QLabel | 跳过已刮削文件： |
| 设置 | `lineEdit_escape_string` | QLineEdit |  |
| 设置 | `label_88` | QLabel | 识别番号时，将先过滤多余字符再进行识别。（填写时以逗号分割，不用区分大小写） |
| 设置 | `checkBox_check_symlink` | QCheckBox | 检查并清理失效的软链接 |
| 设置 | `checkBox_check_symlink_definition` | QCheckBox | 获取软链接指向的原文件的分辨率 |
| 设置 | `label_94` | QLabel | 用于过滤本地的一些广告视频，此处填写文件大小，小于该大小的视频将跳过刮削 |
| 设置 | `label_83` | QLabel | 过滤文件名多余字符： |
| 设置 | `label_93` | QLabel | 跳过小文件(MB) <： |
| 设置 | `groupBox_61` | QGroupBox | 文件清理设置 |
| 设置 | `lineEdit_clean_file_ext` | QLineEdit |  |
| 设置 | `checkBox_clean_file_ext` | QCheckBox | 启用 |
| 设置 | `label_177` | QLabel | 扩展名等于： |
| 设置 | `label_184` | QLabel | 文件名包含： |
| 设置 | `lineEdit_clean_excluded_file_ext` | QLineEdit |  |
| 设置 | `checkBox_clean_excluded_file_ext` | QCheckBox | 启用 |
| 设置 | `label_178` | QLabel | 文件名等于： |
| 设置 | `label_262` | QLabel | ⚠️ 清理文件规则 |
| 设置 | `lineEdit_clean_file_contains` | QLineEdit |  |
| 设置 | `checkBox_clean_file_contains` | QCheckBox | 启用 |
| 设置 | `label_199` | QLabel | 以下已启用的规则中有任一命中时，文件将被清理。（多个内容以｜分割，区分大小写） |
| 设置 | `label_261` | QLabel | 文件名包含： |
| 设置 | `label_270` | QLabel | ⚠️ 不清理文件规则 |
| 设置 | `lineEdit_clean_excluded_file_contains` | QLineEdit |  |
| 设置 | `checkBox_clean_excluded_file_contains` | QCheckBox | 启用 |
| 设置 | `label_202` | QLabel | 扩展名等于： |
| 设置 | `label_263` | QLabel | 文件大小(KB)<=： |
| 设置 | `label_162` | QLabel | 以下已启用的规则中有任一命中时，文件将不被清理。（会优先处理不清理文件规则） |
| 设置 | `lineEdit_clean_file_size` | QLineEdit |  |
| 设置 | `checkBox_clean_file_size` | QCheckBox | 启用 |
| 设置 | `lineEdit_clean_file_name` | QLineEdit |  |
| 设置 | `checkBox_clean_file_name` | QCheckBox | 启用 |
| 设置 | `pushButton_check_and_clean_files` | QPushButton | 点击检查待刮削目录并清理文件 |
| 设置 | `checkBox_auto_clean` | QCheckBox | 刮削时自动清理 |
| 设置 | `checkBox_i_agree_clean` | QCheckBox | 我已同意：无论出现任何问题，均与开发者无关，后果自行承担。 |
| 设置 | `checkBox_i_understand_clean` | QCheckBox | 我已知晓：文件删除后无法恢复！操作须谨慎！ |
| 设置 | `label_271` | QLabel | ⚠️ 使用前请确认规则是否已启用！！！不启用不生效！！！ |
| 设置 | `groupBox_9` | QGroupBox | 文件格式设置 |
| 设置 | `lineEdit_movie_type` | QLineEdit |  |
| 设置 | `label_78` | QLabel | 字幕格式： |
| 设置 | `lineEdit_sub_type` | QLineEdit |  |
| 设置 | `label_50` | QLabel | 视频格式： |
| 设置 | `groupBox` | QGroupBox | 刮削模式 |
| 设置 | `radioButton_mode_sort` | QRadioButton | 视频模式 |
| 设置 | `label_312` | QLabel | 不刮削，读取本地信息并显示，适合检查媒体库或媒体库重新整理分类 |
| 设置 | `pushButton_tips_read_mode` | QPushButton |  |
| 设置 | `radioButton_mode_common` | QRadioButton | 正常模式 |
| 设置 | `checkBox_read_has_nfo_update` | QCheckBox | 本地已刮削成功的文件，重新整理分类（按更新模式规则） |
| 设置 | `label_345` | QLabel | 无需联网 |
| 设置 | `checkBox_read_update_nfo` | QCheckBox | 允许更新 nfo 文件 |
| 设置 | `label_37` | QLabel | <p>将按 下方「Emby视频标题」、「设置」-「翻译」、<br>「设置」-「NFO」等的设置项，利 |
| 设置 | `checkBox_read_download_file_again` | QCheckBox | 重新下载图片等文件（nfo 需有链接） |
| 设置 | `label_347` | QLabel | 将按「设置」-「下载」，更新文件 |
| 设置 | `checkBox_read_no_nfo_scrape` | QCheckBox | 本地没有nfo的文件，重新刮削（按正常模式规则） |
| 设置 | `label_nfo_merge_strategy` | QLabel | NFO合并策略: |
| 设置 | `comboBox_nfo_merge_strategy` | QComboBox |  |
| 设置 | `label_36` | QLabel | 流程同正常模式，但命名按照更新模式规则执行（在下方设置），适合二次刮削 |
| 设置 | `pushButton_tips_update_mode` | QPushButton |  |
| 设置 | `radioButton_mode_read` | QRadioButton | 读取模式 |
| 设置 | `radioButton_mode_update` | QRadioButton | 更新模式 |
| 设置 | `label_15` | QLabel | 执行：刮削->重命名，仅整理本地视频，不下载图片，适合不要海报墙的情况 |
| 设置 | `pushButton_tips_sort_mode` | QPushButton |  |
| 设置 | `checkBox_sortmode_delpic` | QCheckBox | 删除本地已下载的图片和 nfo 文件 |
| 设置 | `label_27` | QLabel | 不勾选，则不删除 |
| 设置 | `label_11` | QLabel | 执行：刮削->下载封面->重命名->水印等全部操作，适合要海报墙的情况 |
| 设置 | `pushButton_tips_normal_mode` | QPushButton |  |
| 设置 | `groupBox_27` | QGroupBox | 刮削成功后移动文件 |
| 设置 | `label_54` | QLabel | 刮削成功时，移动文件到成功输出目录 |
| 设置 | `label_55` | QLabel | 刮削成功时，不移动文件位置，仍在原目录（适合已整理好文件夹或二次刮削场景） |
| 设置 | `radioButton_succ_move_on` | QRadioButton | 开 |
| 设置 | `radioButton_succ_move_off` | QRadioButton | 关 |
| 设置 | `groupBox_15` | QGroupBox | 刮削失败时移动文件 |
| 设置 | `label_34` | QLabel | 刮削失败后，移动文件到失败输出目录 |
| 设置 | `label_35` | QLabel | 刮削失败后，不移动文件位置，仍在原目录 |
| 设置 | `radioButton_fail_move_on` | QRadioButton | 开 |
| 设置 | `radioButton_fail_move_off` | QRadioButton | 关 |
| 设置 | `groupBox_30` | QGroupBox | 刮削结束后删除空文件夹 |
| 设置 | `label_44` | QLabel | 刮削结束后，删除刮削目录中的所有空文件夹 |
| 设置 | `label_51` | QLabel | 刮削结束后，不删除空文件夹 |
| 设置 | `radioButton_del_empty_folder_on` | QRadioButton | 开 |
| 设置 | `radioButton_del_empty_folder_off` | QRadioButton | 关 |
| 设置 | `groupBox_5` | QGroupBox | 更新模式规则 |
| 设置 | `label_218` | QLabel | D目录命名规则 |
| 设置 | `lineEdit_update_d_folder` | QLineEdit |  |
| 设置 | `label_14` | QLabel | 更新视频同级目录下的内容，即：../A/B/C[NEW].mp4 |
| 设置 | `label_20` | QLabel | 在视频所在目录下为视频创建D目录，并更新C内容，即：../A/B/D/C[NEW].mp4 |
| 设置 | `label_278` | QLabel | C文件命名规则 |
| 设置 | `lineEdit_update_c_filetemplate` | QLineEdit |  |
| 设置 | `label_210` | QLabel | B目录命名规则 |
| 设置 | `lineEdit_update_b_folder` | QLineEdit |  |
| 设置 | `radioButton_update_b_c` | QRadioButton | 更新B和C |
| 设置 | `label_25` | QLabel | 更新视频所在目录及该目录下的内容，即：../A/B[NEW]/C[NEW].mp4 |
| 设置 | `radioButton_update_d_c` | QRadioButton | 创建D目录 |
| 设置 | `radioButton_update_c` | QRadioButton | 只更新C |
| 设置 | `checkBox_update_a` | QCheckBox | 同时更新A目录 |
| 设置 | `lineEdit_update_a_folder` | QLineEdit |  |
| 设置 | `label_294` | QLabel | Emby视频标题 |
| 设置 | `lineEdit_update_titletemplate` | QLineEdit |  |
| 设置 | `label_12` | QLabel | 假定视频文件现在的路径是： ../A/B/C.mp4 |
| 设置 | `label_21` | QLabel | <p style='line-height:20px'>⚠️ 保留文件：请到 设置 > 下载 > 保 |
| 设置 | `groupBox_18` | QGroupBox | 刮削成功后重命名文件 |
| 设置 | `label_38` | QLabel | 刮削成功时，按「命名」-「视频命名规则」-「视频文件名」重命名文件 |
| 设置 | `label_39` | QLabel | 刮削成功时，继续使用原来文件名 |
| 设置 | `radioButton_succ_rename_on` | QRadioButton | 开 |
| 设置 | `radioButton_succ_rename_off` | QRadioButton | 关 |
| 设置 | `groupBox_53` | QGroupBox | 多线程刮削 |
| 设置 | `label_237` | QLabel | javdb延时(秒) |
| 设置 | `label_26` | QLabel | 设置 javdb 延时可降低 javdb 被封概率，将在1/2延时-1延时之间随机。 |
| 设置 | `label_82` | QLabel | 线程数量 |
| 设置 | `label_238` | QLabel | 线程间隔(秒) |
| 设置 | `groupBox_2` | QGroupBox | 刮削成功后在输出目录创建软链接或硬链接 |
| 设置 | `radioButton_soft_off` | QRadioButton | 关 |
| 设置 | `radioButton_soft_on` | QRadioButton | 创建软链接 |
| 设置 | `label_link_off` | QLabel | <span>适合 NAS 和硬盘用户。本地党可随心所欲整理文件。<br>注意：选择此项，下面的「成功 |
| 设置 | `radioButton_hard_on` | QRadioButton | 创建硬链接 |
| 设置 | `label_softlink` | QLabel | <span>适合网盘用户。刮削资料存本地，Emby 加载快，网盘读写少。<br>注意：Windows |
| 设置 | `pushButton_tips_soft` | QPushButton |  |
| 设置 | `label_hardlink` | QLabel | <span>适合 PT 用户。刮削资料同盘单独存放，不影响分享率。<br>注意：Mac 用户，请选择 |
| 设置 | `pushButton_tips_hard` | QPushButton |  |
| 设置 | `label_342` | QLabel | 注：软硬链接不会移动和重命名原视频文件，仅移动和重命名链接文件 |
| 设置 | `groupBox_80` | QGroupBox | 类型刮削网站 |
| 设置 | `lineEdit_website_oumei` | QLineEdit |  |
| 设置 | `label_151` | QLabel | 无码番号： |
| 设置 | `label_316` | QLabel | 动漫里番： |
| 设置 | `lineEdit_website_fc2` | QLineEdit |  |
| 设置 | `label_322` | QLabel | Mywife： |
| 设置 | `label_232` | QLabel | <span>「网站偏好」-「指定网站」指定 madouqu、madou_club，或文件路径含有「国 |
| 设置 | `label_156` | QLabel | 比如：259LUXU-1111 |
| 设置 | `label_157` | QLabel | 比如：FC2-111111 |
| 设置 | `label_158` | QLabel | 比如：sexart.11.11.11 |
| 设置 | `lineEdit_website_wuma` | QLineEdit |  |
| 设置 | `lineEdit_website_suren` | QLineEdit |  |
| 设置 | `label_149` | QLabel | 欧美番号： |
| 设置 | `label_155` | QLabel | 比如：111111-111，111111_111，n1111，HEYZO-1111，SMD-111 |
| 设置 | `label_318` | QLabel | <p>「网站偏好」-「指定网站」指定 getchu、dmm，或文件路径含有「里番」、「动漫」时，将自 |
| 设置 | `label_323` | QLabel | <p>「网站偏好」-「指定网站」指定 mywife，或文件路径含有 mywife时，将自动使用 my |
| 设置 | `label_154` | QLabel | 比如：MIDE-111，以及不符合以下类型的番号 |
| 设置 | `label_152` | QLabel | 素人番号： |
| 设置 | `lineEdit_website_youma` | QLineEdit |  |
| 设置 | `label_153` | QLabel | 有码番号： |
| 设置 | `label_148` | QLabel | FC2番号： |
| 设置 | `lineEdit_website_guochan` | QLineEdit |  |
| 设置 | `label_217` | QLabel | 国产番号： |
| 设置 | `comboBox_fixed_scraping_type` | QComboBox |  |
| 设置 | `label_fixed_scraping_type` | QLabel | 锁定刮削类型： |
| 设置 | `label_fixed_scraping_type_desc` | QLabel | 选择后跳过自动类型识别，所有番号直接使用指定类型的网站列表刮削。 |
| 设置 | `pushButton_edit_website_youma` | QPushButton | 编辑网站 |
| 设置 | `pushButton_priority_website_youma` | QPushButton | 字段优先级 |
| 设置 | `pushButton_edit_website_wuma` | QPushButton | 编辑网站 |
| 设置 | `pushButton_priority_website_wuma` | QPushButton | 字段优先级 |
| 设置 | `pushButton_edit_website_suren` | QPushButton | 编辑网站 |
| 设置 | `pushButton_priority_website_suren` | QPushButton | 字段优先级 |
| 设置 | `pushButton_edit_website_fc2` | QPushButton | 编辑网站 |
| 设置 | `pushButton_priority_website_fc2` | QPushButton | 字段优先级 |
| 设置 | `pushButton_edit_website_oumei` | QPushButton | 编辑网站 |
| 设置 | `pushButton_priority_website_oumei` | QPushButton | 字段优先级 |
| 设置 | `pushButton_edit_website_guochan` | QPushButton | 编辑网站 |
| 设置 | `pushButton_priority_website_guochan` | QPushButton | 字段优先级 |
| 设置 | `groupBox_35` | QGroupBox | 字段刮削网站 |
| 设置 | `lineEdit_actors_website` | QLineEdit |  |
| 设置 | `label_114` | QLabel | 标题： |
| 设置 | `lineEdit_title_website` | QLineEdit |  |
| 设置 | `lineEdit_outline_website` | QLineEdit |  |
| 设置 | `lineEdit_poster_website` | QLineEdit |  |
| 设置 | `label_227` | QLabel | 导演： |
| 设置 | `label_182` | QLabel | 发行时间： |
| 设置 | `lineEdit_extrafanart_website` | QLineEdit |  |
| 设置 | `lineEdit_score_website` | QLineEdit |  |
| 设置 | `label_129` | QLabel | 原始标题： |
| 设置 | `label_406` | QLabel | 简介： |
| 设置 | `lineEdit_originaltitle_website` | QLineEdit |  |
| 设置 | `label_191` | QLabel | 封面（大）： |
| 设置 | `label_183` | QLabel | 评分： |
| 设置 | `label_144` | QLabel | 标签： |
| 设置 | `lineEdit_runtime_website` | QLineEdit |  |
| 设置 | `lineEdit_wanted_website` | QLineEdit |  |
| 设置 | `lineEdit_studio_website` | QLineEdit |  |
| 设置 | `label_211` | QLabel | 片商： |
| 设置 | `lineEdit_tags_website` | QLineEdit |  |
| 设置 | `label_180` | QLabel | 剧照： |
| 设置 | `label_307` | QLabel | 想看人数： |
| 设置 | `label_222` | QLabel | 发行商： |
| 设置 | `lineEdit_originalplot_website` | QLineEdit |  |
| 设置 | `label_142` | QLabel | 原始简介： |
| 设置 | `lineEdit_publisher_website` | QLineEdit |  |
| 设置 | `lineEdit_directors_website` | QLineEdit |  |
| 设置 | `label_229` | QLabel | 封面（小）： |
| 设置 | `lineEdit_thumb_website` | QLineEdit |  |
| 设置 | `label_143` | QLabel | 女演员： |
| 设置 | `lineEdit_release_website` | QLineEdit |  |
| 设置 | `label_181` | QLabel | 时长： |
| 设置 | `label_206` | QLabel | 预告片： |
| 设置 | `label_201` | QLabel | 系列： |
| 设置 | `lineEdit_series_website` | QLineEdit |  |
| 设置 | `lineEdit_trailer_website` | QLineEdit |  |
| 设置 | `lineEdit_all_actors_website` | QLineEdit |  |
| 设置 | `label_179` | QLabel | 所有演员： |
| 设置 | `label_325` | QLabel | <p>说明：对于某个字段，如果不指定刮削网站，则将使用任意已获取网站的数据；否则将依次使用字段刮削网 |
| 设置 | `groupBox_11` | QGroupBox | 网站偏好 |
| 设置 | `radioButton_scrape_single` | QRadioButton | 指定网站 |
| 设置 | `label_32` | QLabel | 按各个字段设置的刮削网站进行刮削，字段来自多个网站。字段全一些。 |
| 设置 | `label_317` | QLabel | 当指定网站时，所有番号将只使用该网站刮削！ |
| 设置 | `radioButton_scrape_info` | QRadioButton | 字段优先 |
| 设置 | `label_28` | QLabel | 按番号类型设置的刮削网站进行刮削，字段来自单个网站。速度快一些。 |
| 设置 | `radioButton_scrape_speed` | QRadioButton | 速度优先 |
| 设置 | `comboBox_website_all` | QComboBox |  |
| 设置 | `label_315` | QLabel | ⚠️ 下载剧照、预告片，请选择「字段优先」或「指定网站」！「速度优先」信息不全！ |
| 设置 | `checkBox_field_priority_try_all_images` | QCheckBox | 是否尝试所有图片 |
| 设置 | `label_field_priority_try_all_images` | QLabel | 字段优先图片下载失败时，继续尝试其它图片候选 |
| 设置 | `pushButton_scrape_note` | QPushButton | 刮削不到？看这里！ |
| 设置 | `label_300` | QLabel | ⚠️ 注意！！！选择「字段优先」时，以下设置才有效！！！ |
| 设置 | `groupBox_24` | QGroupBox | 下载 |
| 设置 | `checkBox_download_poster` | QCheckBox | 封面图 |
| 设置 | `checkBox_download_thumb` | QCheckBox | 缩略图 |
| 设置 | `checkBox_download_fanart` | QCheckBox | 背景图 |
| 设置 | `checkBox_download_extrafanart` | QCheckBox | 剧照 |
| 设置 | `checkBox_download_trailer` | QCheckBox | 预告片 |
| 设置 | `checkBox_download_nfo` | QCheckBox | nfo |
| 设置 | `checkBox_compress_downloaded_images` | QCheckBox | 压缩 |
| 设置 | `checkBox_ignore_pic_fail` | QCheckBox | 图片下载失败时，不视为刮削失败 |
| 设置 | `label_275` | QLabel | 有时图片已被源网站删除，此时会下载失败 |
| 设置 | `checkBox_ignore_youma` | QCheckBox | 有码封面不裁剪，直接复制缩略图 |
| 设置 | `label_326` | QLabel | 有码封面可以裁剪，如不想裁剪可以勾选 |
| 设置 | `checkBox_poster_auto_best` | QCheckBox | 有码 Poster 竖图按大小自动选优 |
| 设置 | `label_poster_auto_best` | QLabel | 仅有码：直下/搜图/右裁剪选优 |
| 设置 | `checkBox_ignore_wuma` | QCheckBox | 无码封面不裁剪，直接复制缩略图 |
| 设置 | `label_273` | QLabel | 无码封面人脸位置不固定，建议手动裁剪或直接复制 |
| 设置 | `checkBox_ignore_oumei` | QCheckBox | 欧美封面不裁剪，直接复制缩略图 |
| 设置 | `label_ignore_oumei` | QLabel | 欧美封面人脸位置不固定，建议手动裁剪或直接复制 |
| 设置 | `checkBox_ignore_fc2` | QCheckBox | FC2 封面不裁剪，直接复制缩略图 |
| 设置 | `label_292` | QLabel | FC2 封面人脸位置不固定，建议手动裁剪或直接复制 |
| 设置 | `checkBox_ignore_guochan` | QCheckBox | 国产封面不裁剪，直接复制缩略图 |
| 设置 | `label_305` | QLabel | 国产封面人脸位置不固定，建议手动裁剪或直接复制 |
| 设置 | `checkBox_ignore_size` | QCheckBox | 预告片下载时，不校验文件大小 |
| 设置 | `label_272` | QLabel | 有时网络返回值不对，校验会导致预告片下载失败 |
| 设置 | `label_85` | QLabel | <p style='line-height:20px'>封面图：poster，当 Emby      |
| 设置 | `label_310` | QLabel | ⚠️ 下载剧照、预告片，请选择「字段优先」或「指定网站」！「速度优先」信息不全！ |
| 设置 | `groupBox_33` | QGroupBox | 保留旧文件 |
| 设置 | `checkBox_old_poster` | QCheckBox | 封面图 |
| 设置 | `checkBox_old_thumb` | QCheckBox | 缩略图 |
| 设置 | `checkBox_old_fanart` | QCheckBox | 背景图 |
| 设置 | `checkBox_old_extrafanart` | QCheckBox | 剧照 |
| 设置 | `checkBox_old_trailer` | QCheckBox | 预告片 |
| 设置 | `checkBox_old_nfo` | QCheckBox | nfo |
| 设置 | `checkBox_old_extrafanart_copy` | QCheckBox | 剧照副本 |
| 设置 | `checkBox_old_theme_videos` | QCheckBox | 主题视频 |
| 设置 | `label_79` | QLabel | <p style='line-height:20px'>勾选时，将使用本地文件（如有），不再重新下载 |
| 设置 | `groupBox_51` | QGroupBox | 创建主题视频 |
| 设置 | `label_87` | QLabel | <p style='line-height:20px'>复制预告片到视频下的 backdrops 目 |
| 设置 | `checkBox_theme_videos` | QCheckBox | 使用预告片作为主题视频 |
| 设置 | `pushButton_add_all_theme_videos` | QPushButton | 添加所有主题视频 |
| 设置 | `pushButton_del_all_theme_videos` | QPushButton | 删除所有主题视频 |
| 设置 | `groupBox_34` | QGroupBox | 创建剧照副本 |
| 设置 | `checkBox_download_extrafanart_copy` | QCheckBox | 额外复制一份剧照图到文件夹 |
| 设置 | `lineEdit_extrafanart_dir` | QLineEdit |  |
| 设置 | `label_59` | QLabel | <p style='line-height:20px'>在 Emby                 |
| 设置 | `pushButton_add_all_extrafanart_copy` | QPushButton | 添加所有剧照副本 |
| 设置 | `pushButton_del_all_extrafanart_copy` | QPushButton | 删除所有剧照副本 |
| 设置 | `groupBox_52` | QGroupBox | 下载高清图 |
| 设置 | `label_92` | QLabel | 将从日亚官网搜索高清封面图；严格校验会对所有 Amazon 结果做相似度比对，可能降低搜图成功率。 |
| 设置 | `checkBox_amazon_big_pic` | QCheckBox | 启用 Amazon 查找高清封面图 |
| 设置 | `label_397` | QLabel | 仅影响 Amazon 高清封面图搜索，不影响普通图片下载 |
| 设置 | `checkBox_amazon_strict_pic_verify` | QCheckBox | 严格校验 Amazon 图片 |
| 设置 | `label_amazon_strict_pic_verify` | QLabel | 对所有 Amazon 结果做图片相似度校验 |
| 设置 | `checkBox_amazon_skip_poster_size_precheck` | QCheckBox | 跳过前置 Poster 大小校验 |
| 设置 | `label_amazon_skip_poster_size_precheck` | QLabel | 不因当前 Poster 已达标跳过 Amazon（DMM >=700px / >=400KB / 不 |
| 设置 | `checkBox_dmm_fallback` | QCheckBox | 官方图源兜底（DMM / MGStage） |
| 设置 | `label_dmm_fallback` | QLabel | 站点图源全部失败时，按番号直构官方 CDN 高清图：DMM 高清封面（自动学习厂牌前缀）与 MGSt |
| 设置 | `groupBox_66` | QGroupBox | 显示剧照 |
| 设置 | `label_333` | QLabel | <p style='line-height:20px'>复制剧照到视频下的 behind the s |
| 设置 | `checkBox_extras` | QCheckBox | 剧照作为附加内容显示 |
| 设置 | `pushButton_add_all_extras` | QPushButton | 为所有视频复制剧照 |
| 设置 | `pushButton_del_all_extras` | QPushButton | 删除所有复制的剧照 |
| 设置 | `groupBox_8` | QGroupBox | 视频命名规则 |
| 设置 | `lineEdit_prevent_char` | QLineEdit |  |
| 设置 | `lineEdit_media_name` | QLineEdit |  |
| 设置 | `label_66` | QLabel | <p                                 style='line-hei |
| 设置 | `label_63` | QLabel | 视频文件名： |
| 设置 | `lineEdit_dir_name` | QLineEdit |  |
| 设置 | `label_43` | QLabel | 视频目录名： |
| 设置 | `label_240` | QLabel | 防屏蔽字符： |
| 设置 | `label_68` | QLabel | 指在 nfo 文件中的标题(title)格式，在 Emby 中作为视频标题显示，支持完整 Jinja |
| 设置 | `label_67` | QLabel | Emby视频标题： |
| 设置 | `label_61` | QLabel | 指本地视频文件的文件名格式，命名字段同上，推荐 {{ number }} |
| 设置 | `label_239` | QLabel | 视频文件命名时，可插入防屏蔽字符到文件名的每个字符之间 |
| 设置 | `lineEdit_local_name` | QLineEdit |  |
| 设置 | `label_name_template_preview` | QLabel | 模板预览： |
| 设置 | `plainTextEdit_name_template_preview` | QPlainTextEdit | {{ number }}{% if studio %} [{{ studio }}]{% endif |
| 设置 | `label_name_template_preview_result` | QLabel | 输入 Jinja2 命名模板后，将在这里显示示例渲染结果和语法状态。 |
| 设置 | `groupBox_38` | QGroupBox | 分集命名规则 |
| 设置 | `label_98` | QLabel | 大写，-CD1、-CD2 |
| 设置 | `radioButton_cd_part_lower` | QRadioButton | -cd1 |
| 设置 | `label_97` | QLabel | 小写，-cd1，-cd2 |
| 设置 | `radioButton_cd_part_upper` | QRadioButton | -CD1 |
| 设置 | `radioButton_cd_part_digital` | QRadioButton | -1 |
| 设置 | `label_349` | QLabel | 数字，-1、-2 |
| 设置 | `label_99` | QLabel | 默认识别分集：-CD1｜-PART1｜-HD1｜-1.mp4 （文件名含有这些字符时将识别其中的分集 |
| 设置 | `checkBox_cd_part_a` | QCheckBox | -A.mp4｜.A.mp4｜12A.mp4 (字母结尾的分集，不含字母C) |
| 设置 | `label_350` | QLabel | 允许识别分集： |
| 设置 | `checkBox_cd_part_01` | QCheckBox | -01.mp4(两位数字结尾的分集) |
| 设置 | `checkBox_cd_part_1_xxx` | QCheckBox | -1 abc.mp4 (数字不在结尾的分集) |
| 设置 | `label_408` | QLabel | 允许识别的分隔符： |
| 设置 | `checkBox_cd_part_space` | QCheckBox | 空格 |
| 设置 | `checkBox_cd_part_underline` | QCheckBox | _ 下划线 |
| 设置 | `checkBox_cd_part_point` | QCheckBox | . 小数点 |
| 设置 | `label_409` | QLabel | 默认识别的分集分隔符：- 短横线 |
| 设置 | `checkBox_cd_part_c` | QCheckBox | -C.mp4｜.C.mp4｜12C.mp4 (字母C结尾的分集，识别为CD3) |
| 设置 | `label_430` | QLabel | 勾选后，-C、.C将识别为CD3，不再识别为字幕 |
| 设置 | `groupBox_77` | QGroupBox | 长度命名规则 |
| 设置 | `lineEdit_file_name_max` | QLineEdit |  |
| 设置 | `label_171` | QLabel | 目录名最大长度： |
| 设置 | `label_167` | QLabel | 演员名最大数量： |
| 设置 | `label_169` | QLabel | <p style='line-height:20px'>指目录名最长字符数（建议不要超过 100，太 |
| 设置 | `label_170` | QLabel | 文件名最大长度： |
| 设置 | `label_172` | QLabel | <p style='line-height:20px'>指文件名最长字符数（建议不要超过 100，太 |
| 设置 | `label_168` | QLabel | 指有多位演员时，命名时最多显示的演员数量。超出的演员将用以下字符替代： |
| 设置 | `lineEdit_folder_name_max` | QLineEdit |  |
| 设置 | `lineEdit_actor_name_max` | QLineEdit |  |
| 设置 | `lineEdit_actor_name_more` | QLineEdit |  |
| 设置 | `groupBox_46` | QGroupBox | 马赛克命名规则 |
| 设置 | `label_285` | QLabel | 指命名时在番号后添加版本命名字符。你也可以使用 moword 字段来调整添加位置 |
| 设置 | `lineEdit_youma_style` | QLineEdit |  |
| 设置 | `label_189` | QLabel | 无码： |
| 设置 | `label_117` | QLabel | <p                           style='line-height:20 |
| 设置 | `lineEdit_wuma_style` | QLineEdit |  |
| 设置 | `label_175` | QLabel | 无码流出： |
| 设置 | `lineEdit_umr_style` | QLineEdit |  |
| 设置 | `label_190` | QLabel | 有码： |
| 设置 | `label_137` | QLabel | <p                           style='line-height:20 |
| 设置 | `label_116` | QLabel | <p                           style='line-height:20 |
| 设置 | `label_174` | QLabel | 无码破解： |
| 设置 | `lineEdit_leak_style` | QLineEdit |  |
| 设置 | `label_145` | QLabel | <p>指有码版本，当视频文件路径中含有「有码」、「有碼」字样时，该文件识别为             |
| 设置 | `label_286` | QLabel | 添加马赛克命名字符： |
| 设置 | `checkBox_foldername_mosaic` | QCheckBox | 视频目录名 |
| 设置 | `checkBox_filename_mosaic` | QCheckBox | 视频文件名 |
| 设置 | `groupBox_37` | QGroupBox | 图片命名规则 |
| 设置 | `radioButton_pic_with_filename` | QRadioButton | 视频文件名-poster.jpg |
| 设置 | `radioButton_pic_no_filename` | QRadioButton | poster.jpg |
| 设置 | `label_95` | QLabel | 视频文件名-thumb.jpg，视频文件名-fanart.jpg |
| 设置 | `label_96` | QLabel | thumb.jpg，fanart.jpg |
| 设置 | `groupBox_62` | QGroupBox | 预告片命名规则 |
| 设置 | `radioButton_trailer_with_filename` | QRadioButton | 视频文件名-trailer.mp4 |
| 设置 | `radioButton_trailer_no_filename` | QRadioButton | trailer.mp4 |
| 设置 | `label_115` | QLabel | 每个视频创建一个「视频名-trailer.mp4」，多分集时会创建多个 |
| 设置 | `label_122` | QLabel | 在视频目录创建「trailers」文件夹，多分集共用一个「trailer.mp4」 |
| 设置 | `groupBox_40` | QGroupBox | 字段命名规则 |
| 设置 | `label_407` | QLabel | 演员： |
| 设置 | `label_146` | QLabel | <p>比如moword(自定义的无码标识),cnword(字幕)将显示为: 番号-流出-C<br>  |
| 设置 | `checkBox_number_del_num` | QCheckBox | 去除素人番号前缀数字（比如：259LUXU-1488 将修改为 LUXU-1488，建议保留） |
| 设置 | `lineEdit_actor_no_name` | QLineEdit |  |
| 设置 | `checkBox_actor_del_char` | QCheckBox | 去除演员名括号中的名字（比如：Rio（柚木ティナ）将修改为 Rio） |
| 设置 | `label_319` | QLabel | 素人番号： |
| 设置 | `label_197` | QLabel | 番号后缀顺序： |
| 设置 | `checkBox_title_del_actor` | QCheckBox | 去除标题后的演员名（个别网站在标题末尾额外多加了演员名，建议去除） |
| 设置 | `lineEdit_release_rule` | QLineEdit |  |
| 设置 | `label_276` | QLabel | 发行日期： |
| 设置 | `label_302` | QLabel | 年: YYYY或YY，月: MM，日:DD，比如: YY.MM.DD 将显示为 22.03.20 |
| 设置 | `lineEdit_suffix_sort` | QLineEdit |  |
| 设置 | `label_100` | QLabel | 当演员名不存在时，在使用演员命名字段命名时，使用以上字符替代 |
| 设置 | `label_320` | QLabel | 标题： |
| 设置 | `label_173` | QLabel | 未知演员： |
| 设置 | `checkBox_actor_fc2_seller` | QCheckBox | FC2 无演员时，使用卖家名字作为演员名字 |
| 设置 | `groupBox_65` | QGroupBox | 画质命名规则 |
| 设置 | `radioButton_definition_height` | QRadioButton | 720P、1080P、4K、8K |
| 设置 | `radioButton_definition_hd` | QRadioButton | HD、FHD、QHD、UHD |
| 设置 | `label_329` | QLabel | 以视频分辨率的高度数值来命名不同画质 |
| 设置 | `label_330` | QLabel | 以视频清晰度的英文缩写来命名不同画质 |
| 设置 | `label_331` | QLabel | <p>说明：qHD=540P，HD=720P/960P，FHD=1080P，QHD=1440P(2K |
| 设置 | `radioButton_videosize_video` | QRadioButton | 读取视频画面的高度 |
| 设置 | `radioButton_videosize_path` | QRadioButton | 使用路径中包含的画质信息 |
| 设置 | `radioButton_videosize_none` | QRadioButton | 不获取分辨率 |
| 设置 | `label_332` | QLabel | 分辨率获取方式： |
| 设置 | `label_357` | QLabel | 添加 4K 字符： |
| 设置 | `checkBox_filename_4k` | QCheckBox | 视频文件名 |
| 设置 | `label_358` | QLabel | 指命名时在番号后添加 4K（仅4K）。你也可以使用 4K 字段来调整添加位置 |
| 设置 | `checkBox_foldername_4k` | QCheckBox | 视频目录名 |
| 设置 | `groupBox_67` | QGroupBox | 其他说明 |
| 设置 | `label_353` | QLabel | 1，多版本显示： |
| 设置 | `label_352` | QLabel | <p>1）Emby 支持多版本显示（类似选集），                           |
| 设置 | `label_351` | QLabel | Emby 分集封面需要每个分集都提供图片，图片命名规则需要选择「视频文件名-poster.jpg」 |
| 设置 | `label_354` | QLabel | 2，分集封面显示： |
| 设置 | `groupBox_trans` | QGroupBox | 翻译引擎 |
| 设置 | `label_81` | QLabel | 翻译引擎： |
| 设置 | `label_baidu_hint` | QLabel | DeepL 与 DeepLX 为独立选项；填写 DeepL API / DeepLX URL / 百 |
| 设置 | `label_baidu_appid` | QLabel | 百度 APP ID： |
| 设置 | `lineEdit_baidu_appid` | QLineEdit |  |
| 设置 | `label_baidu_key` | QLabel | 百度密钥： |
| 设置 | `lineEdit_baidu_key` | QLineEdit |  |
| 设置 | `checkBox_google` | QCheckBox | Google |
| 设置 | `checkBox_deepl` | QCheckBox | DeepL |
| 设置 | `checkBox_deeplx` | QCheckBox | DeepLX |
| 设置 | `checkBox_llm` | QCheckBox | LLM |
| 设置 | `checkBox_bing` | QCheckBox | Bing |
| 设置 | `checkBox_baidu` | QCheckBox | 百度 |
| 设置 | `label_164` | QLabel | 当勾选多个时，将随机使用所勾选的其中任一翻译引擎，可降低被封几率 |
| 设置 | `lineEdit_deepl_key` | QLineEdit |  |
| 设置 | `label_deepl_api_key` | QLabel | DeepL API Key： |
| 设置 | `lineEdit_deeplx_url` | QLineEdit |  |
| 设置 | `label_80` | QLabel | DeepLX URL： |
| 设置 | `groupBox_llm` | QGroupBox | LLM 翻译 |
| 设置 | `lineEdit_llm_url` | QLineEdit |  |
| 设置 | `label_llm_url` | QLabel | API URL: |
| 设置 | `label_llm_url_desc` | QLabel | 示例: https://api.openai.com/v1 |
| 设置 | `label_llm_model` | QLabel | Model: |
| 设置 | `lineEdit_llm_model` | QLineEdit |  |
| 设置 | `label_llm_key` | QLabel | API Key: |
| 设置 | `lineEdit_llm_key` | QLineEdit |  |
| 设置 | `label_llm_prompt_title` | QLabel | 标题 Prompt: |
| 设置 | `label_llm_prompt_outline` | QLabel | 简介 Prompt: |
| 设置 | `label_llm_prompt_desc` | QLabel | 提示词模板. 可用变量: {content} 原文 {lang} 目标语言 |
| 设置 | `doubleSpinBox_llm_max_req_sec` | QDoubleSpinBox |  |
| 设置 | `label_llm_max_req_sec` | QLabel | 最大请求速率(/秒): |
| 设置 | `label_llm_max_req_sec_desc` | QLabel | 根据你使用的 API 提供商的限制设定 |
| 设置 | `spinBox_llm_max_try` | QSpinBox |  |
| 设置 | `label_llm_max_try` | QLabel | 最大尝试次数: |
| 设置 | `label_llm_max_try_desc` | QLabel | API 请求失败可能只是因为暂时限流, 因此可多重试几次 |
| 设置 | `label_llm_temperature` | QLabel | Temperature: |
| 设置 | `doubleSpinBox_llm_temperature` | QDoubleSpinBox |  |
| 设置 | `checkBox_llm_disable_thinking` | QCheckBox | 关闭思考模式 |
| 设置 | `label_llm_disable_thinking_desc` | QLabel | 按服务商自动下发关闭思考参数(硅基流动/百炼/火山方舟/Ollama/Gemini), 不支持时自动 |
| 设置 | `groupBox_82` | QGroupBox | 标题 |
| 设置 | `checkBox_title_translate` | QCheckBox | 使用翻译引擎翻译标题 |
| 设置 | `label_242` | QLabel | 标题语言： |
| 设置 | `label_74` | QLabel | 将优先使用刮削网站的中文翻译，当刮削页面无中文时，才使用以下翻译方式。 |
| 设置 | `radioButton_title_zh_cn` | QRadioButton | 中文简体 |
| 设置 | `radioButton_title_zh_tw` | QRadioButton | 中文繁体 |
| 设置 | `radioButton_title_jp` | QRadioButton | 日语 |
| 设置 | `label_244` | QLabel | 翻译方式： |
| 设置 | `groupBox_83` | QGroupBox | 简介 |
| 设置 | `label_133` | QLabel | 简介语言： |
| 设置 | `label_176` | QLabel | 当字段语言选择中文，但只刮削到日语时，可使用翻译引擎进行翻译 |
| 设置 | `label_166` | QLabel | 翻译方式： |
| 设置 | `radioButton_outline_zh_cn` | QRadioButton | 中文简体 |
| 设置 | `radioButton_outline_zh_tw` | QRadioButton | 中文繁体 |
| 设置 | `radioButton_outline_jp` | QRadioButton | 日语 |
| 设置 | `checkBox_outline_translate` | QCheckBox | 使用翻译引擎翻译简介 |
| 设置 | `checkBox_show_translate_from` | QCheckBox | 显示翻译来源 |
| 设置 | `radioButton_trans_show_zh_jp` | QRadioButton | 中文+日语 |
| 设置 | `radioButton_trans_show_jp_zh` | QRadioButton | 日语+中文 |
| 设置 | `radioButton_trans_show_one` | QRadioButton | 关闭 |
| 设置 | `label_328` | QLabel | 双语显示： |
| 设置 | `groupBox_84` | QGroupBox | 演员 |
| 设置 | `label_250` | QLabel | 翻译方式： |
| 设置 | `radioButton_actor_zh_cn` | QRadioButton | 中文简体 |
| 设置 | `radioButton_actor_zh_tw` | QRadioButton | 中文繁体 |
| 设置 | `radioButton_actor_jp` | QRadioButton | 日语 |
| 设置 | `label_249` | QLabel | <p style='line-height:20px'>                       |
| 设置 | `checkBox_actor_realname` | QCheckBox | 使用AV-wiki获取演员真实名字 |
| 设置 | `checkBox_actor_translate` | QCheckBox | 使用演员映射表翻译演员 |
| 设置 | `label_248` | QLabel | 演员语言： |
| 设置 | `groupBox_85` | QGroupBox | 标签 |
| 设置 | `radioButton_tag_zh_cn` | QRadioButton | 中文简体 |
| 设置 | `radioButton_tag_zh_tw` | QRadioButton | 中文繁体 |
| 设置 | `radioButton_tag_jp` | QRadioButton | 日语 |
| 设置 | `label_165` | QLabel | 映射表文件名：info_database.xlsx。作用和演员映射表类似，说明可参考演员映射表。 |
| 设置 | `checkBox_tag_translate` | QCheckBox | 使用信息映射表翻译标签 |
| 设置 | `label_251` | QLabel | 标签语言： |
| 设置 | `label_253` | QLabel | 翻译方式： |
| 设置 | `groupBox_86` | QGroupBox | 系列 |
| 设置 | `label_255` | QLabel | 系列语言： |
| 设置 | `label_256` | QLabel | 翻译方式： |
| 设置 | `label_245` | QLabel | 映射表文件名：info_database.xlsx。作用和演员映射表类似，说明可参考演员映射表。 |
| 设置 | `radioButton_series_zh_cn` | QRadioButton | 中文简体 |
| 设置 | `radioButton_series_zh_tw` | QRadioButton | 中文繁体 |
| 设置 | `radioButton_series_jp` | QRadioButton | 日语 |
| 设置 | `checkBox_series_translate` | QCheckBox | 使用信息映射表翻译系列 |
| 设置 | `groupBox_87` | QGroupBox | 片商 |
| 设置 | `label_259` | QLabel | 片商语言： |
| 设置 | `label_260` | QLabel | 翻译方式： |
| 设置 | `label_247` | QLabel | 映射表文件名：info_database.xlsx。作用和演员映射表类似，说明可参考演员映射表。 |
| 设置 | `radioButton_studio_zh_cn` | QRadioButton | 中文简体 |
| 设置 | `radioButton_studio_zh_tw` | QRadioButton | 中文繁体 |
| 设置 | `radioButton_studio_jp` | QRadioButton | 日语 |
| 设置 | `checkBox_studio_translate` | QCheckBox | 使用信息映射表翻译片商 |
| 设置 | `groupBox_88` | QGroupBox | 发行商 |
| 设置 | `label_264` | QLabel | 发行商语言： |
| 设置 | `label_265` | QLabel | 翻译方式： |
| 设置 | `label_266` | QLabel | 映射表文件名：info_database.xlsx。作用和演员映射表类似，说明可参考演员映射表。 |
| 设置 | `radioButton_publisher_zh_cn` | QRadioButton | 中文简体 |
| 设置 | `radioButton_publisher_zh_tw` | QRadioButton | 中文繁体 |
| 设置 | `radioButton_publisher_jp` | QRadioButton | 日语 |
| 设置 | `checkBox_publisher_translate` | QCheckBox | 使用信息映射表翻译发行商 |
| 设置 | `groupBox_89` | QGroupBox | 导演 |
| 设置 | `label_267` | QLabel | 发行商语言： |
| 设置 | `label_268` | QLabel | 翻译方式： |
| 设置 | `label_269` | QLabel | 映射表文件名：info_database.xlsx。作用和演员映射表类似，说明可参考演员映射表。 |
| 设置 | `checkBox_director_translate` | QCheckBox | 使用信息映射表翻译导演 |
| 设置 | `radioButton_director_zh_cn` | QRadioButton | 中文简体 |
| 设置 | `radioButton_director_zh_tw` | QRadioButton | 中文繁体 |
| 设置 | `radioButton_director_jp` | QRadioButton | 日语 |
| 设置 | `groupBox_20` | QGroupBox | 中文字幕字符规则 |
| 设置 | `lineEdit_cnword_style` | QLineEdit |  |
| 设置 | `label_89` | QLabel | 中文字幕判断字符： |
| 设置 | `lineEdit_cnword_char` | QLineEdit |  |
| 设置 | `label_90` | QLabel | 指视频有中文字幕时，在重命名文件名及目录名时在番号后添加该字符表示有中文字幕 |
| 设置 | `label_91` | QLabel | <p                                 style='line-hei |
| 设置 | `label_69` | QLabel | 中文字幕命名字符： |
| 设置 | `label_119` | QLabel | 指命名时在番号后添加中文字幕命名字符。你也可以使用 cnword 字段来调整添加位置 |
| 设置 | `checkBox_foldername` | QCheckBox | 视频目录名 |
| 设置 | `checkBox_filename` | QCheckBox | 视频文件名 |
| 设置 | `label_120` | QLabel | 添加中文字幕字符： |
| 设置 | `groupBox_45` | QGroupBox | 添加外挂字幕 |
| 设置 | `label_113` | QLabel | 刮削时，如果视频无内嵌字幕且同目录无字幕文件，则从字幕文件目录查找并复制字幕 |
| 设置 | `label_102` | QLabel | 下载字幕包解压，填写字幕文件目录的路径 |
| 设置 | `label_download_sub_zip` | QLabel | 点击下载字幕包 |
| 设置 | `label_111` | QLabel | 字幕文件目录： |
| 设置 | `label_112` | QLabel | 刮削时自动添加字幕： |
| 设置 | `radioButton_add_sub_on` | QRadioButton | 开 |
| 设置 | `radioButton_add_sub_off` | QRadioButton | 关 |
| 设置 | `lineEdit_sub_folder` | QLineEdit |  |
| 设置 | `pushButton_select_subtitle_folder` | QPushButton | 选择目录 |
| 设置 | `pushButton_add_sub_for_all_video` | QPushButton | 点击检查所有视频的字幕情况并为无字幕视频添加字幕 |
| 设置 | `label_125` | QLabel | <p                           style='line-height:20 |
| 设置 | `checkBox_sub_add_chs` | QCheckBox | 字幕文件名添加.chs后缀 |
| 设置 | `checkBox_sub_rescrape` | QCheckBox | 新添加字幕的视频在结束后重新刮削 |
| 设置 | `groupBox_26` | QGroupBox | 自定义水印样式 |
| 设置 | `label_118` | QLabel | <p                           style='line-height:20 |
| 设置 | `label_download_mark_zip` | QLabel | 点击下载水印图片包 |
| 设置 | `groupBox_31` | QGroupBox | 水印设置 |
| 设置 | `radioButton_not_fixed_position` | QRadioButton | 不固定位置 |
| 设置 | `radioButton_fixed_corner` | QRadioButton | 固定一个位置 |
| 设置 | `radioButton_fixed_position` | QRadioButton | 固定不同位置 |
| 设置 | `label_138` | QLabel | <p                                 style='line-hei |
| 设置 | `label_135` | QLabel | 水印类型： |
| 设置 | `label_128` | QLabel | 添加水印的图片： |
| 设置 | `checkBox_sub` | QCheckBox | 字幕 |
| 设置 | `checkBox_censored` | QCheckBox | 有码 |
| 设置 | `checkBox_umr` | QCheckBox | 破解 |
| 设置 | `checkBox_leak` | QCheckBox | 流出 |
| 设置 | `checkBox_uncensored` | QCheckBox | 无码 |
| 设置 | `checkBox_hd` | QCheckBox | 4K/8K |
| 设置 | `label_140` | QLabel | 水印图片的显示高度 = 设置的水印大小 / 40 * 封面图高度 |
| 设置 | `label_141` | QLabel | <p                                 style='line-hei |
| 设置 | `checkBox_poster_mark` | QCheckBox | poster |
| 设置 | `checkBox_thumb_mark` | QCheckBox | thumb |
| 设置 | `checkBox_fanart_mark` | QCheckBox | fanart |
| 设置 | `label_139` | QLabel | 水印大小： |
| 设置 | `label_127` | QLabel | 水印位置： |
| 设置 | `label_130` | QLabel | Emby 中 fanart 作为背景图，不需要添加水印。其他软件作为预览图时，可添加水印 |
| 设置 | `groupBox_36` | QGroupBox | 不固定位置 |
| 设置 | `radioButton_top_left` | QRadioButton | 左上 |
| 设置 | `radioButton_top_right` | QRadioButton | 右上 |
| 设置 | `radioButton_bottom_right` | QRadioButton | 右下 |
| 设置 | `radioButton_bottom_left` | QRadioButton | 左下 |
| 设置 | `label_126` | QLabel | 首个水印位置： |
| 设置 | `groupBox_42` | QGroupBox | 固定不同位置 |
| 设置 | `radioButton_top_left_sub` | QRadioButton | 左上 |
| 设置 | `radioButton_top_right_sub` | QRadioButton | 右上 |
| 设置 | `radioButton_bottom_right_sub` | QRadioButton | 右下 |
| 设置 | `radioButton_bottom_left_sub` | QRadioButton | 左下 |
| 设置 | `label_131` | QLabel | 字幕水印位置： |
| 设置 | `radioButton_top_left_mosaic` | QRadioButton | 左上 |
| 设置 | `radioButton_top_right_mosaic` | QRadioButton | 右上 |
| 设置 | `radioButton_bottom_right_mosaic` | QRadioButton | 右下 |
| 设置 | `radioButton_bottom_left_mosaic` | QRadioButton | 左下 |
| 设置 | `label_134` | QLabel | 马赛克水印位置： |
| 设置 | `radioButton_top_left_hd` | QRadioButton | 左上 |
| 设置 | `radioButton_top_right_hd` | QRadioButton | 右上 |
| 设置 | `radioButton_bottom_right_hd` | QRadioButton | 右下 |
| 设置 | `radioButton_bottom_left_hd` | QRadioButton | 左下 |
| 设置 | `label_216` | QLabel | 4K/8K水印位置： |
| 设置 | `groupBox_39` | QGroupBox | 固定一个位置 |
| 设置 | `radioButton_top_left_corner` | QRadioButton | 左上 |
| 设置 | `radioButton_top_right_corner` | QRadioButton | 右上 |
| 设置 | `radioButton_bottom_right_corner` | QRadioButton | 右下 |
| 设置 | `radioButton_bottom_left_corner` | QRadioButton | 左下 |
| 设置 | `label_233` | QLabel | 水印显示位置： |
| 设置 | `groupBox_81` | QGroupBox | 写入 NFO 的字段： |
| 设置 | `checkBox_nfo_all_actor` | QCheckBox | 写入男女演员（不勾选，则仅写入女演员） |
| 设置 | `checkBox_nfo_actor_tmdbid` | QCheckBox | 为演员写入 TMDB ID（需配置 TMDB API） |
| 设置 | `label_391` | QLabel | 年份/时长/想看人数： |
| 设置 | `checkBox_tag_letters` | QCheckBox | 番号前缀 |
| 设置 | `checkBox_tag_actor` | QCheckBox | 演员 |
| 设置 | `checkBox_tag_definition` | QCheckBox | 分辨率 |
| 设置 | `checkBox_tag_cnword` | QCheckBox | 中文字幕 |
| 设置 | `label_396` | QLabel | 请填写 Tagline 格式： |
| 设置 | `lineEdit_nfo_tagline` | QLineEdit | 发行日期：release |
| 设置 | `checkBox_nfo_sorttitle` | QCheckBox | 类标题（sorttitle） |
| 设置 | `checkBox_nfo_originaltitle` | QCheckBox | 原标题（originaltitle） |
| 设置 | `checkBox_nfo_genre` | QCheckBox | 风格（使用标签字段） |
| 设置 | `checkBox_nfo_actor_set` | QCheckBox | 合集（使用演员字段） |
| 设置 | `checkBox_nfo_set` | QCheckBox | 合集（使用系列字段） |
| 设置 | `checkBox_nfo_poster` | QCheckBox | 封面（poster） |
| 设置 | `checkBox_nfo_cover` | QCheckBox | 背景（cover） |
| 设置 | `checkBox_nfo_trailer` | QCheckBox | 预告片（trilaer） |
| 设置 | `checkBox_nfo_website` | QCheckBox | 网址（website） |
| 设置 | `label_163` | QLabel | 标题： |
| 设置 | `label_388` | QLabel | 片商/发行商： |
| 设置 | `checkBox_nfo_outline` | QCheckBox | 简介（outline） |
| 设置 | `checkBox_nfo_plot` | QCheckBox | 简介（plot） |
| 设置 | `checkBox_nfo_originalplot` | QCheckBox | 原简介（originalplot） |
| 设置 | `label_412` | QLabel | 标签中系列的格式： |
| 设置 | `lineEdit_nfo_tag_series` | QLineEdit | 系列: series |
| 设置 | `label_416` | QLabel | 标签中片商的格式： |
| 设置 | `lineEdit_nfo_tag_studio` | QLineEdit | 片商: studio |
| 设置 | `checkBox_outline_cdata` | QCheckBox | 简介不写入 <![CDATA[*]]> 标记 |
| 设置 | `label_390` | QLabel | 评分： |
| 设置 | `checkBox_nfo_score` | QCheckBox | 公众评分（score） |
| 设置 | `checkBox_nfo_criticrating` | QCheckBox | 影评人评分（criticrating） |
| 设置 | `checkBox_nfo_studio` | QCheckBox | 片商（studio） |
| 设置 | `checkBox_nfo_maker` | QCheckBox | 片商（maker） |
| 设置 | `checkBox_nfo_publisher` | QCheckBox | 发行商（publisher） |
| 设置 | `checkBox_nfo_label` | QCheckBox | 发行商（label） |
| 设置 | `checkBox_tag_mosaic` | QCheckBox | 有码/无码 |
| 设置 | `checkBox_tag_series` | QCheckBox | 系列 |
| 设置 | `checkBox_tag_studio` | QCheckBox | 片商 |
| 设置 | `checkBox_tag_publisher` | QCheckBox | 发行商 |
| 设置 | `checkBox_nfo_series` | QCheckBox | 系列（series） |
| 设置 | `checkBox_nfo_tag` | QCheckBox | 标签（tag） |
| 设置 | `label_384` | QLabel | 简介： |
| 设置 | `label_208` | QLabel | 系列/标签： |
| 设置 | `label_418` | QLabel | 标签中发行的格式： |
| 设置 | `lineEdit_nfo_tag_publisher` | QLineEdit | 发行: publisher |
| 设置 | `checkBox_nfo_release` | QCheckBox | 发行日期（release） |
| 设置 | `checkBox_nfo_relasedate` | QCheckBox | 发行日期（releasedate） |
| 设置 | `checkBox_nfo_premiered` | QCheckBox | 发行日期（premiered） |
| 设置 | `label_334` | QLabel | 风格/合集： |
| 设置 | `label_385` | QLabel | 发行日期： |
| 设置 | `label_392` | QLabel | 国家/分级： |
| 设置 | `checkBox_nfo_year` | QCheckBox | 年份（year） |
| 设置 | `checkBox_nfo_runtime` | QCheckBox | 时长（runtime） |
| 设置 | `checkBox_nfo_wanted` | QCheckBox | 想看人数（votes） |
| 设置 | `checkBox_nfo_title_cd` | QCheckBox | 标题末尾写入分集信息 |
| 设置 | `checkBox_nfo_country` | QCheckBox | 国家（country） |
| 设置 | `checkBox_nfo_mpaa` | QCheckBox | 分级信息（mpaa） |
| 设置 | `checkBox_nfo_customrating` | QCheckBox | 自定义分级（customrating） |
| 设置 | `label_386` | QLabel | 演员/导演： |
| 设置 | `checkBox_nfo_actor` | QCheckBox | 演员（actor） |
| 设置 | `checkBox_nfo_director` | QCheckBox | 导演（director） |
| 设置 | `label_395` | QLabel | 请勾选写入标签的信息： |
| 设置 | `label_150` | QLabel | 封面/背景/预告片： |
| 设置 | `label_423` | QLabel | 标签中演员的格式： |
| 设置 | `lineEdit_nfo_tag_actor` | QLineEdit | actor |
| 设置 | `label_428` | QLabel | 注意：如果需要繁体，请到「设置」-「翻译」-「标签」，勾选为繁体！ |
| 设置 | `label_389` | QLabel | 注：同一字段多个名称可以兼容更多类型版本的媒体库 |
| 设置 | `pushButton_field_tips_nfo` | QPushButton | 字段说明 |
| 设置 | `groupBox_43` | QGroupBox | Emby/Jellyfin 设置 |
| 设置 | `lineEdit_user_id` | QLineEdit |  |
| 设置 | `label_104` | QLabel | 服务器地址： |
| 设置 | `label_105` | QLabel | API 密钥创建方法：控制台->高级->API 密钥->添加（APP 名称任意） |
| 设置 | `comboBox_pic_actor` | QComboBox |  |
| 设置 | `pushButton_show_pic_actor` | QPushButton | 查看 |
| 设置 | `radioButton_server_emby` | QRadioButton | Emby |
| 设置 | `radioButton_server_jellyfin` | QRadioButton | Jellyfin |
| 设置 | `lineEdit_emby_url` | QLineEdit |  |
| 设置 | `label_298` | QLabel | 查看信息： |
| 设置 | `label_121` | QLabel | 指你的 Emby/Jellyfin 服务器地址，比如：http://192.168.1.5:8096 |
| 设置 | `label_306` | QLabel | 服务器类型： |
| 设置 | `label_108` | QLabel | 用户 ID： |
| 设置 | `label_107` | QLabel | API 密钥： |
| 设置 | `lineEdit_api_key` | QLineEdit |  |
| 设置 | `label_109` | QLabel | 如果设置，将仅获取指定 Emby/Jellyfin 用户媒体库中的演员 |
| 设置 | `groupBox_41` | QGroupBox | 补全 Emby/Jellyfin 演员头像 |
| 设置 | `pushButton_add_actor_pic` | QPushButton | 开始补全 |
| 设置 | `label_297` | QLabel | 使用网络头像库或本地头像库，补全 Emby/Jellyfin 演员头像。 |
| 设置 | `checkBox_actor_photo_auto` | QCheckBox | 刮削结束后自动补全演员头像 |
| 设置 | `radioButton_actor_photo_all` | QRadioButton | 所有女优 |
| 设置 | `radioButton_actor_photo_miss` | QRadioButton | 仅缺少头像的女优 |
| 设置 | `label_296` | QLabel | 补全范围： |
| 设置 | `label_77` | QLabel | 下载头像包解压，填写头像图片目录的路径 |
| 设置 | `label_293` | QLabel | 头像来源： |
| 设置 | `label_101` | QLabel | 本地头像库： |
| 设置 | `checkBox_actor_photo_ne_backdrop` | QCheckBox | 使用 Graphis 背景 |
| 设置 | `checkBox_actor_photo_ne_face` | QCheckBox | 使用 Graphis 头像 |
| 设置 | `checkBox_actor_photo_ne_new` | QCheckBox | 请求 Graphis 最新图片 |
| 设置 | `lineEdit_net_actor_photo` | QLineEdit |  |
| 设置 | `radioButton_actor_photo_net` | QRadioButton | 网络头像库（Gfriends） |
| 设置 | `radioButton_actor_photo_local` | QRadioButton | 本地头像库 |
| 设置 | `label_download_actor_zip` | QLabel | 点击下载头像包 |
| 设置 | `lineEdit_actor_photo_folder` | QLineEdit |  |
| 设置 | `pushButton_select_actor_photo_folder` | QPushButton | 选择目录 |
| 设置 | `label_303` | QLabel | 网络头像库： |
| 设置 | `label_123` | QLabel | <p>支持优先使用 Graphis.ne.jp 的图片作为演员头像和演员背景；<br>Graphis |
| 设置 | `label_gfriends_local` | QLabel | Gfriends 本地仓库： |
| 设置 | `lineEdit_gfriends_local_path` | QLineEdit |  |
| 设置 | `pushButton_select_gfriends_local` | QPushButton | 选择目录 |
| 设置 | `pushButton_sync_gfriends` | QPushButton | 更新 Gfriends |
| 设置 | `label_gfriends_update_time` | QLabel | 最后更新: - |
| 设置 | `groupBox_64` | QGroupBox | 补全 Emby/Jellyfin 演员信息 |
| 设置 | `radioButton_actor_info_zh_cn` | QRadioButton | 中文简体 |
| 设置 | `radioButton_actor_info_zh_tw` | QRadioButton | 中文繁体 |
| 设置 | `radioButton_actor_info_ja` | QRadioButton | 日语 |
| 设置 | `label_431` | QLabel | 演员信息数据库： |
| 设置 | `lineEdit_actor_db_path` | QLineEdit |  |
| 设置 | `pushButton_select_actor_info_db` | QPushButton | 选择文件 |
| 设置 | `checkBox_actor_db` | QCheckBox | 使用数据库补全演员信息 |
| 设置 | `label_download_actor_db` | QLabel | 点击下载演员数据库 |
| 设置 | `label_291` | QLabel | 补全语言： |
| 设置 | `checkBox_actor_info_translate` | QCheckBox | 不存在中文时，翻译日语为中文 |
| 设置 | `label_106` | QLabel | 不勾选则无中文时使用日语 |
| 设置 | `pushButton_add_actor_info` | QPushButton | 开始补全 |
| 设置 | `label_295` | QLabel | 使用minnano-av和维基百科补全Emby/Jellyfin演员信息，包括:生日、身高、三围、出 |
| 设置 | `radioButton_actor_info_all` | QRadioButton | 所有女优 |
| 设置 | `radioButton_actor_info_miss` | QRadioButton | 仅缺少信息的女优 |
| 设置 | `label_299` | QLabel | 补全范围： |
| 设置 | `checkBox_actor_info_photo` | QCheckBox | 补全完成后自动补全演员头像 |
| 设置 | `groupBox_68` | QGroupBox | 补全 Kodi/Plex/Jvedio 演员头像 |
| 设置 | `pushButton_add_actor_pic_kodi` | QPushButton | 开始补全 |
| 设置 | `label_414` | QLabel | 将为待刮削目录的每个视频在同目录创建一个 .actors 文件夹，并将该视频的演员图片放在该文件夹中 |
| 设置 | `checkBox_actor_pic_replace` | QCheckBox | 覆盖已存在的演员图片 |
| 设置 | `label_415` | QLabel | 图片已存在时： |
| 设置 | `pushButton_del_actor_folder` | QPushButton | 清除所有 .actors 文件夹 |
| 设置 | `checkBox_actor_photo_kodi` | QCheckBox | 刮削结束后自动创建 |
| 设置 | `groupBox_10` | QGroupBox | Cookie设置 |
| 设置 | `label_45` | QLabel | javdb： （登录状态） |
| 设置 | `plainTextEdit_cookie_javdb` | QPlainTextEdit | 刮削FC2需要填写 |
| 设置 | `pushButton_check_javdb_cookie` | QPushButton | 检查cookie |
| 设置 | `label_425` | QLabel | javbus： （登录状态） |
| 设置 | `plainTextEdit_cookie_javbus` | QPlainTextEdit | 美国节点需要填写，其他节点一般不需要填写，除非提示需要填写。 |
| 设置 | `pushButton_check_javbus_cookie` | QPushButton | 检查cookie |
| 设置 | `label_fc2ppvdb_cookie` | QLabel | fc2ppvdb： （登录状态） |
| 设置 | `plainTextEdit_cookie_fc2ppvdb` | QPlainTextEdit | 请粘贴 fc2cmadb.com 登录后的完整 Cookie（含 XSRF-TOKEN 与 sess |
| 设置 | `pushButton_check_fc2ppvdb_cookie` | QPushButton | 检查cookie |
| 设置 | `label_75` | QLabel | <p style='line-height:20px'>Cookie 获取方法：<br>       |
| 设置 | `label_get_cookie_url` | QLabel | https://tieba.baidu.com/p/5492736764 |
| 设置 | `label_7` | QLabel | 演示动画： |
| 设置 | `groupBox_28` | QGroupBox | 网络设置 |
| 设置 | `label_103` | QLabel | <p style='line-height:20px'>支持 http(s), socks5(h)  |
| 设置 | `checkBox_use_proxy` | QCheckBox | 使用代理 |
| 设置 | `label_73` | QLabel | 超时时间： |
| 设置 | `lineEdit_proxy` | QLineEdit |  |
| 设置 | `label_no_proxy_sites` | QLabel | 使用代理： |
| 设置 | `comboBox_no_proxy_sites` | QComboBox |  |
| 设置 | `lineEdit_no_proxy_sites` | QLineEdit | 逗号分隔，如 api.tmdb.org,libredmm |
| 设置 | `checkBox_proxy_route_all` | QCheckBox | 全部走代理 |
| 设置 | `label_cf_bypass` | QLabel | CF Bypass： |
| 设置 | `lineEdit_cf_bypass_url` | QLineEdit | 留空则由外部 CF 服务自动启动（高级：手动指定 cf_bypasser 协议服务地址） |
| 设置 | `label_cf_bypass_proxy` | QLabel | CF Bypass代理： |
| 设置 | `lineEdit_cf_bypass_proxy` | QLineEdit | 例如: http://127.0.0.1:7890（可选） |
| 设置 | `label_cf_bypass_trawl` | QLabel | 外部 CF 服务： |
| 设置 | `lineEdit_cf_bypass_trawl_url` | QLineEdit | 例如: http://127.0.0.1:8191 |
| 设置 | `comboBox_cf_bypass_backend` | QComboBox |  |
| 设置 | `label_cf_bypass_trusted_hosts` | QLabel | Bypass落地白名单： |
| 设置 | `lineEdit_cf_bypass_trusted_hosts` | QLineEdit | 逗号分隔，如 javbus.com,*.javdb.com（留空不校验） |
| 设置 | `label_cf_bypass_trusted_hosts_desc` | QLabel | 用途：校验 Bypass 服务落地/重定向后的最终域名，防止第三方服务被劫持时把恶意页面当数据。支持 |
| 设置 | `label_65` | QLabel | 重试次数： |
| 设置 | `label_64` | QLabel | 代理地址： |
| 设置 | `label_verify_ssl` | QLabel | HTTPS 证书校验： |
| 设置 | `checkBox_verify_ssl` | QCheckBox | 启用 HTTPS 证书校验（自签名代理 / MITM 调试时关闭） |
| 设置 | `groupBox_44` | QGroupBox | 网站设置 |
| 设置 | `label_401` | QLabel | 当前网站： |
| 设置 | `comboBox_custom_website` | QComboBox |  |
| 设置 | `lineEdit_site_custom_url` | QLineEdit |  |
| 设置 | `label_132` | QLabel | <p>可在下方设置选定网站的配置。<span style=" color:#d9001f;">切换网 |
| 设置 | `label_400` | QLabel | 自定义网址： |
| 设置 | `label_110` | QLabel | <html><head/><body><p>自定义指定网站的网址，刮削时将用其代替默认网址</p>< |
| 设置 | `label_136` | QLabel | <html><head/><body><p>必须安装 Chrome 浏览器。可处理某些无法获取的网站 |
| 设置 | `groupBox_14` | QGroupBox | API Token |
| 设置 | `label_355` | QLabel | ThePornDB： |
| 设置 | `lineEdit_api_token_theporndb` | QLineEdit |  |
| 设置 | `label_423_wl` | QLabel | TMDB API地址： |
| 设置 | `lineEdit_tmdb_api_base` | QLineEdit | api.tmdb.org |
| 设置 | `label_424_wl` | QLabel | TMDB API Key： |
| 设置 | `lineEdit_tmdb_api_key` | QLineEdit |  |
| 设置 | `label_356` | QLabel | <html><head/><body><p><a                           |
| 设置 | `checkBox_theporndb_hash` | QCheckBox | 不使用Hash值匹配数据 |
| 设置 | `label_422` | QLabel | <html><head/><body><p>该网站的Hash值匹配结果可能错误</p></body> |
| 设置 | `groupBox_17` | QGroupBox | 保存日志 |
| 设置 | `radioButton_log_on` | QRadioButton | 开 |
| 设置 | `radioButton_log_off` | QRadioButton | 关 |
| 设置 | `groupBox_3` | QGroupBox | 调试模式（日志页面） |
| 设置 | `checkBox_show_web_log` | QCheckBox | 显示刮削过程信息 |
| 设置 | `checkBox_show_from_log` | QCheckBox | 显示字段来源信息 |
| 设置 | `checkBox_show_data_log` | QCheckBox | 显示字段内容信息 |
| 设置 | `groupBox_4` | QGroupBox | 检查更新 |
| 设置 | `radioButton_update_on` | QRadioButton | 开 |
| 设置 | `radioButton_update_off` | QRadioButton | 关 |
| 设置 | `groupBox_12` | QGroupBox | 高级功能 |
| 设置 | `checkBox_hide_window_title` | QCheckBox | 隐藏边框（美观样式） |
| 设置 | `checkBox_dark_mode` | QCheckBox | 暗黑模式 |
| 设置 | `checkBox_hide_dock_icon` | QCheckBox | 隐藏 Dock 图标（Mac） |
| 设置 | `label_42` | QLabel | 保存后重启软件生效 |
| 设置 | `checkBox_hide_menu_icon` | QCheckBox | 隐藏菜单栏图标（Mac） |
| 设置 | `label_321` | QLabel | 间歇刮削： |
| 设置 | `checkBox_auto_start` | QCheckBox | 启动软件后自动开始刮削 |
| 设置 | `checkBox_auto_exit` | QCheckBox | 刮削结束后自动退出软件 |
| 设置 | `checkBox_show_dialog_exit` | QCheckBox | 退出软件时 |
| 设置 | `checkBox_show_dialog_stop_scrape` | QCheckBox | 停止刮削时 |
| 设置 | `checkBox_timed_scrape` | QCheckBox | 每隔 |
| 设置 | `lineEdit_timed_interval` | QLineEdit |  |
| 设置 | `label_84` | QLabel | （时:分:秒），自动开始刮削（读取配置时开始计时） |
| 设置 | `label_308` | QLabel | 自动任务： |
| 设置 | `label_309` | QLabel | 自动刮削： |
| 设置 | `label_277` | QLabel | 弹窗确认： |
| 设置 | `lineEdit_config_folder` | QLineEdit |  |
| 设置 | `pushButton_select_config_folder` | QPushButton | 选择目录 |
| 设置 | `checkBox_remain_task` | QCheckBox | 记住未完成的刮削任务，即使退出或中止，下次仍可继续刮削未完成任务 |
| 设置 | `label_279` | QLabel | 保留任务： |
| 设置 | `label_40` | QLabel | 将读取该目录中的配置文件、映射表、水印图片、演员头像等数据，修改后重启程序方可生效 |
| 设置 | `checkBox_dialog_qt` | QCheckBox | 使用 QT 选择对话框 |
| 设置 | `label_421` | QLabel | 目录中的文件较多时，可以勾选此项以提高打开速度 |
| 设置 | `label_314` | QLabel | 隐藏图标： |
| 设置 | `label_243` | QLabel | 配置文件目录： |
| 设置 | `radioButton_hide_close` | QRadioButton | 点关闭按钮 |
| 设置 | `radioButton_hide_mini` | QRadioButton | 点最小化按钮 |
| 设置 | `radioButton_hide_none` | QRadioButton | 无 |
| 设置 | `checkBox_rest_scrape` | QCheckBox | 连续刮削 |
| 设置 | `lineEdit_rest_count` | QLineEdit |  |
| 设置 | `label_52` | QLabel | 个文件后，自动休息 |
| 设置 | `lineEdit_rest_time` | QLineEdit |  |
| 设置 | `label_71` | QLabel | （时:分:秒） |
| 设置 | `label_313` | QLabel | 隐藏窗口： |
| 设置 | `label_246` | QLabel | 界面外观： |
| 设置 | `label_420` | QLabel | 选择对话框： |
| 设置 | `label_426` | QLabel | 高分屏缩放： |
| 设置 | `comboBox_ui_scale` | QComboBox |  |
| 设置 | `label_427` | QLabel | 保存后重启软件生效，可能会有点模糊 |
| 设置 | `pushButton_init_config` | QPushButton | 恢复默认 |
| 设置 | `pushButton_save_config` | QPushButton | 保存 |
| 设置 | `comboBox_change_config` | QComboBox |  |
| 设置 | `label_241` | QLabel | 当前配置： |
| 设置 | `pushButton_save_new_config` | QPushButton | 另存为 |
| 设置 | `textBrowser_show_success_list` | QTextBrowser |  |
| 设置 | `pushButton_success_list_close` | QPushButton | 关闭 |
| 设置 | `pushButton_success_list_clear` | QPushButton | 清空列表 |
| 设置 | `pushButton_success_list_save` | QPushButton | 保存 |
| 设置 | `label_success_title` | QLabel | 已刮削成功文件列表 |
| 设置 | `textBrowser_show_tips` | QTextBrowser |  |
| 设置 | `pushButton_show_tips_close` | QPushButton | 关闭 |
| 设置 | `label_show_tips_title` | QLabel | 说明 |
| 关于 | `textBrowser_about` | QTextBrowser |  |
| NFO库 | `pushButton_nfo_lib_select_dir` | QPushButton | 选择目录 |
| NFO库 | `lineEdit_nfo_lib_dir` | QLineEdit | 点击"选择目录"选择 NFO 所在文件夹 |
| NFO库 | `label_nfo_lib_count` | QLabel | 共 0 个 |
| NFO库 | `lineEdit_nfo_lib_filter` | QLineEdit | 筛选番号/演员/标题... |
| NFO库 | `pushButton_nfo_lib_refresh` | QPushButton | 刷新 |
| NFO库 | `label_nfo_lib_list_title` | QLabel | NFO 文件列表 |
| NFO库 | `listWidget_nfo_lib` | QListWidget |  |
| NFO库 | `groupBox_nfo_lib_batch` | QGroupBox | 批量操作（选中多条后使用） |
| NFO库 | `pushButton_nfo_lib_batch_actor` | QPushButton | 替换演员名 |
| NFO库 | `lineEdit_nfo_lib_batch_actor` | QLineEdit | 新演员名（逗号分隔） |
| NFO库 | `pushButton_nfo_lib_batch_add_tag` | QPushButton | 加标签 |
| NFO库 | `lineEdit_nfo_lib_batch_add_tag` | QLineEdit | 标签（逗号分隔） |
| NFO库 | `pushButton_nfo_lib_batch_del_tag` | QPushButton | 删标签 |
| NFO库 | `lineEdit_nfo_lib_batch_del_tag` | QLineEdit | 标签（逗号分隔） |
| NFO库 | `pushButton_nfo_lib_batch_series` | QPushButton | 统一系列名 |
| NFO库 | `lineEdit_nfo_lib_batch_series` | QLineEdit | 系列名 |
| NFO库 | `pushButton_nfo_lib_batch_save` | QPushButton | 批量保存 |
| NFO库 | `label_nfo_lib_batch_hint` | QLabel | 用法：先在左侧 NFO 列表选中多条记录，再填写内容点对应按钮（替换演员名/加标签/删标签/统一系列 |
| NFO库 | `label_nfo_lib_number` | QLabel | 番号 |
| NFO库 | `lineEdit_nfo_lib_number` | QLineEdit |  |
| NFO库 | `label_nfo_lib_title` | QLabel | 标题 |
| NFO库 | `lineEdit_nfo_lib_title` | QLineEdit |  |
| NFO库 | `label_nfo_lib_actor` | QLabel | 演员 |
| NFO库 | `lineEdit_nfo_lib_actor` | QLineEdit |  |
| NFO库 | `label_nfo_lib_release` | QLabel | 发行日 |
| NFO库 | `lineEdit_nfo_lib_release` | QLineEdit |  |
| NFO库 | `label_nfo_lib_year` | QLabel | 年份 |
| NFO库 | `lineEdit_nfo_lib_year` | QLineEdit |  |
| NFO库 | `label_nfo_lib_runtime` | QLabel | 时长 |
| NFO库 | `lineEdit_nfo_lib_runtime` | QLineEdit |  |
| NFO库 | `label_nfo_lib_director` | QLabel | 导演 |
| NFO库 | `lineEdit_nfo_lib_director` | QLineEdit |  |
| NFO库 | `label_nfo_lib_studio` | QLabel | 制作商 |
| NFO库 | `lineEdit_nfo_lib_studio` | QLineEdit |  |
| NFO库 | `label_nfo_lib_publisher` | QLabel | 发行商 |
| NFO库 | `lineEdit_nfo_lib_publisher` | QLineEdit |  |
| NFO库 | `label_nfo_lib_series` | QLabel | 系列 |
| NFO库 | `lineEdit_nfo_lib_series` | QLineEdit |  |
| NFO库 | `label_nfo_lib_score` | QLabel | 评分 |
| NFO库 | `lineEdit_nfo_lib_score` | QLineEdit |  |
| NFO库 | `label_nfo_lib_outline` | QLabel | 简介 |
| NFO库 | `label_nfo_lib_tag` | QLabel | 标签 |
| NFO库 | `label_nfo_lib_cover_url` | QLabel | 封面URL |
| NFO库 | `lineEdit_nfo_lib_cover_url` | QLineEdit |  |
| NFO库 | `label_nfo_lib_poster_url` | QLabel | 海报URL |
| NFO库 | `lineEdit_nfo_lib_poster_url` | QLineEdit |  |
| NFO库 | `pushButton_nfo_lib_save` | QPushButton | 保存当前 NFO |
| NFO库 | `label_nfo_lib_poster_preview` | QLabel | 海报预览 |
| NFO库 | `label_nfo_lib_thumb_preview` | QLabel | 缩略图预览 |
| NFO库 | `pushButton_nfo_lib_crop` | QPushButton | 裁剪封面 |

## 每页控件数

- 影片刮削: 25
- 日志: 8
- 网络检测: 5
- 工具: 88
- 设置: 851
- 关于: 1
- NFO库: 50
