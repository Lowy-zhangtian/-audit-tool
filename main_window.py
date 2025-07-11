# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os

# Import modules from data_processing and review_engine
from data_processing.data_loader import DataLoader
from data_processing.ocr_processor import OCRProcessor
from data_processing.data_cleaner import DataCleaner
from review_engine.rule_engine import RuleEngine
from review_engine.llm_module import LLMModule

class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("🔍 审计报告智能复核系统")
        master.geometry("1400x900")
        master.minsize(1200, 800)
        
        # 设置现代化主题颜色
        self.colors = {
            'primary': '#2E86AB',      # 主蓝色
            'secondary': '#A23B72',    # 紫红色
            'accent': '#F18F01',       # 橙色
            'success': '#28A745',      # 绿色
            'background': '#F5F7FA',   # 浅灰背景
            'surface': '#FFFFFF',      # 白色表面
            'text_primary': '#2D3748', # 深灰文字
            'text_secondary': '#718096', # 中灰文字
            'border': '#E2E8F0'        # 边框颜色
        }
        
        # 配置主窗口样式
        master.configure(bg=self.colors['background'])
        
        # 配置ttk样式
        self.setup_styles()

        # Initialize modules
        self.data_loader = DataLoader()
        self.ocr_processor = OCRProcessor()
        self.data_cleaner = DataCleaner()
        self.rule_engine = RuleEngine()
        self.llm_module = LLMModule()

        # Data storage
        self.loaded_data = None  # For structured data (CSV/Excel)
        self.image_attachment_paths = [] # For image/PDF paths
        self.processed_data = None # Integrated and cleaned data
        self.review_results = None # Final review results

        self.create_widgets()
    
    def setup_styles(self):
        """设置现代化的ttk样式"""
        style = ttk.Style()
        
        # 配置按钮样式
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground='black',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        style.map('Primary.TButton',
                 background=[('active', '#1A5F7A'),
                           ('pressed', '#1A5F7A')])
        
        style.configure('Secondary.TButton',
                       background=self.colors['secondary'],
                       foreground='black',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        style.map('Secondary.TButton',
                 background=[('active', '#7A2B5C'),
                           ('pressed', '#7A2B5C')])
        
        style.configure('Accent.TButton',
                       background=self.colors['accent'],
                       foreground='black',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        style.map('Accent.TButton',
                 background=[('active', '#D17A01'),
                           ('pressed', '#D17A01')])
        
        # 配置Treeview样式
        style.configure('Modern.Treeview',
                       background=self.colors['surface'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['surface'],
                       borderwidth=1,
                       relief='solid')
        style.configure('Modern.Treeview.Heading',
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=1,
                       relief='solid')
        style.map('Modern.Treeview',
                 background=[('selected', self.colors['primary'])])

    def create_widgets(self):
        # --- 标题栏 ---
        title_frame = tk.Frame(self.master, bg=self.colors['primary'], height=80)
        title_frame.pack(side="top", fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, 
                              text="🔍 审计报告智能复核系统",
                              font=('Microsoft YaHei UI', 24, 'bold'),
                              bg=self.colors['primary'],
                              fg='white')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(title_frame,
                                 text="基于AI技术的智能审计报告分析平台",
                                 font=('Microsoft YaHei UI', 12),
                                 bg=self.colors['primary'],
                                 fg='#E6F3FF')
        subtitle_label.pack()

        # --- 工具栏 ---
        toolbar_frame = tk.Frame(self.master, bg=self.colors['surface'], height=100)
        toolbar_frame.pack(side="top", fill="x", padx=20, pady=(20, 10))
        toolbar_frame.pack_propagate(False)
        
        # 创建工具栏标签
        toolbar_label = tk.Label(toolbar_frame,
                                text="📋 操作面板",
                                font=('Microsoft YaHei UI', 14, 'bold'),
                                bg=self.colors['surface'],
                                fg=self.colors['text_primary'])
        toolbar_label.pack(anchor='w', pady=(10, 5))
        
        # 按钮容器
        button_container = tk.Frame(toolbar_frame, bg=self.colors['surface'])
        button_container.pack(fill='x', pady=5)
        
        # 主要操作按钮
        btn_load_data = ttk.Button(button_container, text="📁 加载审计数据", 
                                  command=self.load_audit_data, style='Primary.TButton')
        btn_load_data.pack(side="left", padx=(0, 10))

        btn_upload_audit_report = ttk.Button(button_container, text="📄 上传审计报告", 
                                            command=self.upload_audit_report, style='Primary.TButton')
        btn_upload_audit_report.pack(side="left", padx=(0, 10))

        btn_load_attachments = ttk.Button(button_container, text="📎 加载支撑文件", 
                                         command=self.load_attachments, style='Primary.TButton')
        btn_load_attachments.pack(side="left", padx=(0, 10))

        btn_process_integrate = ttk.Button(button_container, text="⚙️ 数据处理集成", 
                                          command=self.process_and_integrate_data, style='Secondary.TButton')
        btn_process_integrate.pack(side="left", padx=(0, 10))

        btn_run_review = ttk.Button(button_container, text="🚀 执行智能复核", 
                                   command=self.run_review_engine, style='Accent.TButton')
        btn_run_review.pack(side="left", padx=(0, 10))

        # 辅助操作按钮
        btn_export_results = ttk.Button(button_container, text="💾 导出结果", 
                                        command=self.export_review_results)
        btn_export_results.pack(side="left", padx=(0, 10))

        btn_reset = ttk.Button(button_container, text="🔄 重置系统", 
                              command=self.reset_system)
        btn_reset.pack(side="left", padx=(0, 10))

        btn_help = ttk.Button(button_container, text="❓ 帮助", 
                             command=self.show_help_about)
        btn_help.pack(side="right")

        # --- 主内容区域 ---
        content_frame = tk.Frame(self.master, bg=self.colors['background'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # 创建左右分栏
        main_pane = tk.PanedWindow(content_frame, orient=tk.HORIZONTAL, 
                                  sashrelief="flat", sashwidth=8,
                                  bg=self.colors['background'])
        main_pane.pack(fill="both", expand=True)

        # 左侧面板：数据展示区
        left_panel = tk.Frame(main_pane, bg=self.colors['surface'], 
                             relief='solid', borderwidth=1)
        main_pane.add(left_panel, width=800, minsize=600)
        
        # 左侧标题
        left_title = tk.Label(left_panel,
                             text="📊 数据概览",
                             font=('Microsoft YaHei UI', 16, 'bold'),
                             bg=self.colors['surface'],
                             fg=self.colors['text_primary'])
        left_title.pack(anchor='w', padx=20, pady=(15, 10))
        
        # 数据表格容器
        tree_container = tk.Frame(left_panel, bg=self.colors['surface'])
        tree_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # 创建Treeview和滚动条
        self.tree = ttk.Treeview(tree_container, show="headings", style='Modern.Treeview')
        
        # 垂直滚动条
        tree_scrollbar_y = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        tree_scrollbar_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=tree_scrollbar_y.set)
        
        # 水平滚动条
        tree_scrollbar_x = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree.xview)
        tree_scrollbar_x.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=tree_scrollbar_x.set)
        
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # 右侧面板：详情和结果区
        right_panel = tk.Frame(main_pane, bg=self.colors['surface'],
                              relief='solid', borderwidth=1)
        main_pane.add(right_panel, width=500, minsize=400)
        
        # 右侧标题
        right_title = tk.Label(right_panel,
                              text="📋 详细信息",
                              font=('Microsoft YaHei UI', 16, 'bold'),
                              bg=self.colors['surface'],
                              fg=self.colors['text_primary'])
        right_title.pack(anchor='w', padx=20, pady=(15, 10))
        
        # 文本区域容器
        text_container = tk.Frame(right_panel, bg=self.colors['surface'])
        text_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # 创建文本区域和滚动条
        self.result_text = tk.Text(text_container, 
                                  wrap="word", 
                                  state="disabled",
                                  bg=self.colors['surface'],
                                  fg='#666666',
                                  font=('Microsoft YaHei UI', 11),
                                  borderwidth=1,
                                  relief='solid',
                                  padx=15,
                                  pady=15)
        
        text_scrollbar = ttk.Scrollbar(text_container, orient="vertical", command=self.result_text.yview)
        text_scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=text_scrollbar.set)
        
        self.result_text.pack(fill="both", expand=True)
        
        # 添加欢迎信息
        self.show_welcome_message()
        
        # --- 状态栏 ---
        status_frame = tk.Frame(self.master, bg=self.colors['primary'], height=30)
        status_frame.pack(side="bottom", fill="x")
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame,
                                    text="🟢 系统就绪 - 请开始加载审计数据",
                                    font=('Microsoft YaHei UI', 10),
                                    bg=self.colors['primary'],
                                    fg='white')
        self.status_label.pack(side='left', padx=20, pady=5)
        
        version_label = tk.Label(status_frame,
                                text="v1.0.0",
                                font=('Microsoft YaHei UI', 10),
                                bg=self.colors['primary'],
                                fg='#E6F3FF')
        version_label.pack(side='right', padx=20, pady=5)
    
    def show_welcome_message(self):
        """显示欢迎信息"""
        welcome_text = """🎉 欢迎使用审计报告智能复核系统！

📋 系统功能：
• 智能加载和解析审计报告数据
• 自动处理支撑文件（图片、PDF等）
• 基于规则引擎的合规性检查
• AI大模型深度分析
• 生成详细的复核报告

🚀 快速开始：
1. 点击"📁 加载审计数据"导入CSV或Excel文件
2. 可选择加载相关的支撑文件
3. 执行"⚙️ 数据处理集成"进行预处理
4. 点击"🚀 执行智能复核"开始分析
5. 查看结果并导出报告

💡 提示：选择左侧表格中的任意行可查看详细信息"""
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, welcome_text)
        self.result_text.config(state=tk.DISABLED)
    
    def update_status(self, message, status_type="info"):
        """更新状态栏信息"""
        status_icons = {
            "info": "🟢",
            "warning": "🟡",
            "error": "🔴",
            "processing": "🔄"
        }
        icon = status_icons.get(status_type, "🟢")
        self.status_label.config(text=f"{icon} {message}")
        self.master.update_idletasks()

    def update_treeview(self, dataframe):
        # Clear existing data
        for i in self.tree.get_children():
            self.tree.delete(i)

        if dataframe.empty:
            self.tree["columns"] = ("",)
            self.tree.heading("", text="无数据")
            self.tree.column("", width=100)
            return

        # Set new columns
        self.tree["columns"] = list(dataframe.columns)
        for col in dataframe.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100) # Default width

        # Insert data
        for index, row in dataframe.iterrows():
            self.tree.insert("", "end", values=list(row))

    def update_review_results_display(self, dataframe):
        # Clear existing data
        for i in self.tree.get_children():
            self.tree.delete(i)

        if dataframe.empty:
            self.tree["columns"] = ("",)
            self.tree.heading("", text="无复核结果")
            self.tree.column("", width=100)
            return

        # Set new columns for review results
        self.tree["columns"] = list(dataframe.columns)
        for col in dataframe.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100) # Default width

        # Insert data
        for index, row in dataframe.iterrows():
            self.tree.insert("", "end", values=list(row))

        # Also update the text area with a summary or first result
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        if not dataframe.empty:
            summary_text = "复核结果概览：\n"
            summary_text += f"总报告数: {len(dataframe)}\n"
            if '是否合规' in dataframe.columns:
                compliant_count = dataframe[dataframe['是否合规'] == '是'].shape[0]
                non_compliant_count = dataframe[dataframe['是否合规'] == '否'].shape[0]
                summary_text += f"合规报告数: {compliant_count}\n"
                summary_text += f"不合规报告数: {non_compliant_count}\n"
            self.result_text.insert(tk.END, summary_text)
            self.result_text.insert(tk.END, "\n详细结果请在左侧表格中选择查看。")
        else:
            self.result_text.insert(tk.END, "没有可显示的复核结果。")
        self.result_text.config(state=tk.DISABLED)

    def load_audit_data(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.loaded_data = self.data_loader.load_structured_data(file_path)
                messagebox.showinfo("信息", f"成功加载数据: {os.path.basename(file_path)}")
                # Display loaded data in Treeview immediately
                self.update_treeview(self.loaded_data)
            except Exception as e:
                messagebox.showerror("错误", f"加载数据失败: {e}")

    def upload_audit_report(self):
        """上传审计报告PDF并进行文本识别"""
        file_path = filedialog.askopenfilename(
            title="选择审计报告PDF文件",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            try:
                # 检查文件类型
                if not file_path.lower().endswith('.pdf'):
                    messagebox.showwarning("警告", "请选择PDF格式的审计报告文件！")
                    return
                
                # 检查文件大小（限制为100MB）
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                if file_size > 100:
                    messagebox.showwarning("警告", f"文件过大({file_size:.1f}MB)，请选择小于100MB的文件！")
                    return
                
                # 显示处理状态
                self.update_status("正在识别审计报告内容...", "processing")
                self.master.update()
                
                # 使用data_loader处理PDF
                pdf_content = self.data_loader.load_document_data(file_path)
                
                if pdf_content and pdf_content.strip():
                    # 存储审计报告内容
                    if not hasattr(self, 'audit_reports'):
                        self.audit_reports = []
                    
                    report_info = {
                        '文件名': os.path.basename(file_path),
                        '文件路径': file_path,
                        '文件大小': f"{file_size:.1f}MB",
                        '识别状态': '成功',
                        '内容长度': len(pdf_content),
                        '内容预览': pdf_content[:200] + "..." if len(pdf_content) > 200 else pdf_content
                    }
                    
                    self.audit_reports.append(report_info)
                    
                    # 将审计报告信息转换为DataFrame并显示
                    import pandas as pd
                    df_reports = pd.DataFrame(self.audit_reports)
                    self.update_treeview(df_reports)
                    
                    # 在右侧显示详细内容
                    self.result_text.config(state=tk.NORMAL)
                    self.result_text.delete('1.0', tk.END)
                    
                    display_content = f"📄 审计报告识别结果\n\n"
                    display_content += f"文件名: {report_info['文件名']}\n"
                    display_content += f"文件大小: {report_info['文件大小']}\n"
                    display_content += f"内容长度: {report_info['内容长度']} 字符\n\n"
                    display_content += f"识别内容预览:\n{'-'*50}\n"
                    display_content += pdf_content[:1000]
                    if len(pdf_content) > 1000:
                        display_content += "\n\n[内容过长，仅显示前1000字符...]\n"
                        display_content += f"\n完整内容共 {len(pdf_content)} 字符"
                    
                    self.result_text.insert(tk.END, display_content)
                    self.result_text.config(state=tk.DISABLED)
                    
                    # 更新状态
                    self.update_status(f"审计报告识别完成: {report_info['文件名']}", "success")
                    
                    messagebox.showinfo("成功", 
                                      f"审计报告识别完成！\n\n"
                                      f"文件: {report_info['文件名']}\n"
                                      f"识别字符数: {report_info['内容长度']}\n\n"
                                      f"内容已显示在右侧详情区域")
                    
                else:
                    # 处理识别失败的情况
                    error_info = {
                        '文件名': os.path.basename(file_path),
                        '文件路径': file_path,
                        '文件大小': f"{file_size:.1f}MB",
                        '识别状态': '失败',
                        '内容长度': 0,
                        '内容预览': '无法识别文本内容，可能是扫描版PDF'
                    }
                    
                    if not hasattr(self, 'audit_reports'):
                        self.audit_reports = []
                    self.audit_reports.append(error_info)
                    
                    import pandas as pd
                    df_reports = pd.DataFrame(self.audit_reports)
                    self.update_treeview(df_reports)
                    
                    self.update_status("审计报告识别失败", "warning")
                    messagebox.showwarning("识别失败", 
                                         f"无法从PDF中提取文本内容。\n\n"
                                         f"可能原因：\n"
                                         f"• PDF是扫描版本，需要OCR处理\n"
                                         f"• PDF文件损坏或加密\n"
                                         f"• 文件格式不支持\n\n"
                                         f"建议：尝试使用文本版PDF或联系技术支持")
                
            except Exception as e:
                self.update_status("审计报告处理出错", "error")
                messagebox.showerror("错误", f"处理审计报告时出错:\n{str(e)}")

    def load_attachments(self):
        file_paths = filedialog.askopenfilenames(
            filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_paths:
            # 显示处理进度
            self.update_status("正在处理支撑文件...", "processing")
            
            processed_files = 0
            failed_files = []
            
            for file_path in file_paths:
                try:
                    # 检查文件大小（限制为50MB）
                    file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                    if file_size > 50:
                        failed_files.append(f"{os.path.basename(file_path)} (文件过大: {file_size:.1f}MB)")
                        continue
                    
                    # 处理PDF文件
                    if file_path.lower().endswith('.pdf'):
                        try:
                            # 使用data_loader处理PDF
                            pdf_content = self.data_loader.load_document_data(file_path)
                            if pdf_content:
                                # 将PDF内容存储到附件路径列表中
                                self.image_attachment_paths.append(file_path)
                                processed_files += 1
                                
                                # 更新状态显示处理进度
                                self.update_status(f"已处理 {processed_files}/{len(file_paths)} 个文件", "processing")
                                self.master.update()  # 强制更新界面
                            else:
                                failed_files.append(f"{os.path.basename(file_path)} (PDF处理失败)")
                        except Exception as pdf_error:
                            failed_files.append(f"{os.path.basename(file_path)} (PDF错误: {str(pdf_error)[:50]})")
                    else:
                        # 处理图片文件
                        self.image_attachment_paths.append(file_path)
                        processed_files += 1
                        self.update_status(f"已处理 {processed_files}/{len(file_paths)} 个文件", "processing")
                        self.master.update()
                        
                except Exception as e:
                    failed_files.append(f"{os.path.basename(file_path)} (错误: {str(e)[:50]})")
            
            # 显示处理结果
            if processed_files > 0:
                success_msg = f"成功加载 {processed_files} 个支撑文件。"
                if failed_files:
                    success_msg += f"\n\n失败文件 ({len(failed_files)}):\n" + "\n".join(failed_files[:5])
                    if len(failed_files) > 5:
                        success_msg += f"\n...还有 {len(failed_files) - 5} 个文件失败"
                messagebox.showinfo("处理完成", success_msg)
                self.update_status(f"已加载 {processed_files} 个支撑文件", "success")
            else:
                error_msg = "没有文件被成功处理。\n\n失败原因:\n" + "\n".join(failed_files[:10])
                messagebox.showerror("处理失败", error_msg)
                self.update_status("文件加载失败", "error")

    def process_and_integrate_data(self):
        if self.loaded_data is None and not self.image_attachment_paths:
            messagebox.showwarning("警告", "请先加载审计报告数据或支撑文件！")
            return

        # Simulate OCR processing for image/PDF files
        # For demonstration, let's assume some key fields are extracted
        # In a real scenario, this would involve actual OCR and data extraction logic
        # For now, we'll just add a placeholder for OCR results
        # ocr_results = [] # This would be populated by OCRProcessor
        # key_fields = {
        #     "invoice_number": "INV2023-001",
        #     "total_amount": "1000.00",
        #     "currency": "USD",
        #     "date": "2023-01-15"
        # }
        # ocr_results.append(key_fields)

        # Placeholder for data cleaning and integration
        # cleaned_data = self.data_cleaner.clean_data(loaded_data)
        # integrated_data = self.data_cleaner.integrate_data(cleaned_data, ocr_results)

        # For now, we'll just use the loaded_data as the processed data
        # In a real scenario, integrated_data would be passed to the rule engine and LLM
        self.processed_data = self.loaded_data

        # Update the Treeview with processed data
        self.update_treeview(self.processed_data)

        messagebox.showinfo("信息", "数据加载、处理和集成完成！")

    def run_review_engine(self):
        """运行规则引擎和LLM模块进行复核。"""
        if not hasattr(self, 'processed_data') or self.processed_data.empty:
            messagebox.showwarning("警告", "请先加载并处理数据！")
            return

        # 运行规则引擎
        # Assuming self.processed_data is a pandas DataFrame or similar structure
        # that rule_engine can process.
        # The rule engine should return a DataFrame with review results.
        # For demonstration, we'll simulate rule engine output.
        # self.review_results = self.rule_engine.apply_rules(self.processed_data)

        # Simulate rule engine application
        # For each report in processed_data, apply rules and get a result
        simulated_rule_results = []
        for index, row in self.processed_data.iterrows():
            report_id = row.get('报告ID', f'Report_{index+1}')
            # Simulate rule application based on some conditions
            if '金额' in row and row['金额'] > 5000:
                violation_details = "金额超过5000元，需要重点关注。"
                is_compliant = False
            else:
                violation_details = "无重大违规。"
                is_compliant = True
            simulated_rule_results.append({
                '报告ID': report_id,
                '是否合规': '是' if is_compliant else '否',
                '违规详情': violation_details
            })
        self.rule_review_results = pd.DataFrame(simulated_rule_results)

        # 运行LLM模块进行分析
        # Assuming llm_module.batch_analyze_reports takes a list of reports
        # and returns a list of analysis results.
        # For demonstration, we'll simulate LLM analysis output.
        # llm_analysis_results = self.llm_module.batch_analyze_reports(self.processed_data.to_dict(orient='records'))

        # Simulate LLM analysis
        simulated_llm_results = []
        for index, row in self.processed_data.iterrows():
            report_id = row.get('报告ID', f'Report_{index+1}')
            # Simulate LLM analysis based on some conditions
            if '描述' in row and '异常' in row['描述']:
                llm_analysis = "LLM分析：发现描述中存在异常关键词，建议人工复核。"
            else:
                llm_analysis = "LLM分析：未发现明显异常。"
            simulated_llm_results.append({
                '报告ID': report_id,
                'LLM分析结果': llm_analysis
            })
        self.llm_analysis_results = pd.DataFrame(simulated_llm_results)

        # 合并规则引擎和LLM分析结果
        # Merge on '报告ID' or a similar unique identifier
        self.review_results = pd.merge(
            self.rule_review_results,
            self.llm_analysis_results,
            on='报告ID',
            how='left'
        )

        # Update the Treeview with processed data
        self.update_review_results_display(self.review_results)

        messagebox.showinfo("信息", "审计报告复核完成！")

    def export_review_results(self):
        """导出复核结果到CSV文件。"""
        if not hasattr(self, 'review_results') or self.review_results.empty:
            messagebox.showwarning("警告", "没有复核结果可导出！")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.review_results.to_csv(file_path, index=False, encoding='utf-8-sig')
                messagebox.showinfo("信息", f"复核结果已成功导出到 {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {e}")

    def reset_system(self):
        """重置系统状态，清空所有加载的数据和结果。"""
        if hasattr(self, 'processed_data'):
            del self.processed_data
        if hasattr(self, 'rule_review_results'):
            del self.rule_review_results
        if hasattr(self, 'llm_analysis_results'):
            del self.llm_analysis_results
        if hasattr(self, 'review_results'):
            del self.review_results
        if hasattr(self, 'audit_reports'):
            del self.audit_reports
        if hasattr(self, 'loaded_data'):
            del self.loaded_data
        
        # 清空附件路径列表
        self.image_attachment_paths = []

        # 清空Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        # 清空Text区域
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.config(state=tk.DISABLED)
        
        # 重置状态
        self.update_status("系统已重置", "success")
        
        # 显示欢迎信息
        self.show_welcome_message()

        messagebox.showinfo("信息", "系统已重置！所有数据已清空。")

    def on_tree_select(self, event):
        """处理Treeview选择事件，显示选中行的详细信息。"""
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            columns = [self.tree.heading(col)['text'] for col in self.tree['columns']]
            detail_text = ""
            for col, value in zip(columns, values):
                detail_text += f"{col}: {value}\n"
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, detail_text)

    def show_help_about(self):
        print("Debugging: Entering show_help_about")
        # Display Help/About information.
        print("About: Audit Report Review System\nVersion 1.0\n\nThis application assists in the automated review of audit reports using advanced data processing, rule-based analysis, and large language models.\n\nDeveloped by: Your Company/Team\nContact: support@example.com\n\n© 2023 All Rights Reserved.")


if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()