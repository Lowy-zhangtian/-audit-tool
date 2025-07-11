# -audit-tool
Audit tools are software solutions that automate data collection, analysis, and verification to support auditing processes in fields like finance and cybersecurity.

# 审计报告复核系统使用说明文档

## 一、系统概述
**审计报告复核系统** 是一个基于Python开发的本地化工具，用于自动化校验审计报告的合规性、逻辑性和数据一致性。系统结合规则引擎和开源大语言模型（LLM），实现对审计报告的智能分析，支持人工复核与机器分析协同工作，提升审计质量控制效率。


## 二、环境要求
### 1. 硬件要求
- **CPU**：建议4核及以上（支持AVX指令集，LLM推理更高效）。  
- **内存**：8GB以上（若运行7B参数模型，建议16GB）。  
- **存储**：50GB可用空间（用于存储模型文件和数据库）。  

### 2. 软件依赖
```bash
python >= 3.9
pandas          # 数据处理
pyqt5           # GUI界面
pdfminer.six     # PDF解析
pytesseract      # OCR识别（需配合Tesseract OCR引擎）
llama-cpp-python # 开源LLM本地推理（支持LLaMA等模型）
sqlalchemy       # 数据库操作
```


## 三、系统架构
### 1. 核心模块
| 模块名称         | 功能描述                                                                 |
|------------------|--------------------------------------------------------------------------|
| **数据处理**     | 解析Excel/PDF/图片文件，提取结构化数据和文本内容，完成数据清洗与标准化。 |
| **规则引擎**     | 执行刚性规则（如数据勾稽关系）和柔性规则（如LLM生成的语义规则）。         |
| **LLM分析**      | 使用本地开源模型（如LLaMA）进行语义理解、合规性检查和风险点识别。         |
| **GUI界面**      | 提供文件管理、结果展示和人工复核功能，支持多标签页切换。                 |
| **数据库**       | 存储审计报告元数据、复核结果和历史记录，支持SQLite/PostgreSQL。          |


## 四、快速开始
### 1. 安装与配置
#### 步骤1：克隆项目
```bash
git clone https://github.com/your-username/audit-report-review-system.git
cd audit-report-review-system
```

#### 步骤2：安装依赖
```bash
pip install -r requirements.txt
```

#### 步骤3：配置本地LLM模型
1. 从[Hugging Face模型库](https://huggingface.co/models)下载LLaMA/Alpaca等模型的GGML量化版本（如`ggml-model-q4_0.bin`）。  
2. 将模型文件放入项目根目录的`models/`文件夹。  
3. 修改`config.py`中的模型路径：  
   ```python
   CONFIG["LLM_MODEL_PATH"] = "models/ggml-model-q4_0.bin"
   ```

#### 步骤4：配置OCR（可选）
- 下载[Tesseract OCR引擎](https://github.com/UB-Mannheim/tesseract/wiki)并安装。  
- 在`config.py`中指定路径（Windows示例）：  
  ```python
  CONFIG["OCR_PATH"] = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
  ```


### 2. 启动系统
```bash
python main.py
```


## 五、界面操作指南
### 1. 主界面布局
![主界面示意图](https://via.placeholder.com/800x400?text=审计报告复核系统界面布局)

#### 区域说明：
- **顶部工具栏**：包含文件操作、复核启动、结果保存按钮。  
- **左侧文件列表**：显示已加载的审计报告文件路径。  
- **右侧结果标签页**：  
  - **规则校验结果**：显示刚性规则执行结果，高风险项标红。  
  - **LLM分析结果**：展示大模型对文本的语义分析和风险识别。  
  - **报告预览**：显示审计报告文本内容或表格数据概览。  
- **底部状态栏**：显示系统状态和操作提示。


### 2. 核心操作流程
#### 步骤1：加载审计报告
1. 点击**打开文件**，选择以下格式文件：  
   - Excel（`.xlsx`/`.xls`）：支持报表数据自动解析。  
   - PDF（`.pdf`）：提取文本内容，支持扫描件OCR识别（需配置Tesseract）。  
   - 图片（`.jpg`/`.png`）：通过OCR提取文字（仅适用于简单报告）。  

#### 步骤2：执行复核
1. 点击**开始复核**，系统将：  
   - 解析文件并清洗数据。  
   - 运行规则引擎（如资产负债表平衡校验）。  
   - 调用本地LLM分析文本逻辑和合规性（如检查审计意见是否明确）。  

#### 步骤3：查看结果
- **规则校验结果**：  
  - 表格显示规则ID、描述、严重程度（高/中/低）和问题详情。  
  - 高风险项背景标红，中风险项标黄。  
- **LLM分析结果**：  
  - 分点列出逻辑漏洞、合规性问题和风险建议（如“结论缺乏数据支持，建议核查原始凭证”）。  

#### 步骤4：保存与导出
1. 点击**保存结果**，将复核报告导出为JSON文件，包含：  
   - 原始文件路径、复核时间。  
   - 规则引擎和LLM分析的详细结果。  
   - 整体状态（通过/不通过/存疑）。  


## 六、系统功能详解
### 1. 数据处理模块
#### 支持的文件类型：
| 文件类型   | 解析方式                                                                 |
|------------|--------------------------------------------------------------------------|
| **Excel**  | 读取所有工作表，自动识别资产负债表、利润表等常见报表结构。               |
| **PDF**    | 文本型PDF直接提取文字；扫描件PDF通过OCR识别（需启用Tesseract）。         |
| **图片**   | 仅支持简单版式的报告图片，通过OCR提取文字（精度有限，建议优先用PDF/Excel）。 |

#### 数据清洗功能：
- 单位转换（如“万元”→“元”）。  
- 数据标准化（统一科目名称、修正OCR识别错误，如“叁仟”→“3000”）。  
- 表格结构识别（自动提取报表中的行、列和数值）。  


### 2. 规则引擎
#### 内置规则列表：
| 规则ID | 规则描述                               | 严重程度 | 示例触发条件                          |
|--------|----------------------------------------|----------|---------------------------------------|
| R001   | 资产负债表不平衡                       | 高       | 资产总计≠负债+所有者权益总计          |
| R002   | 净利润与未分配利润变动不一致           | 中       | 利润表净利润≠资产负债表未分配利润变动 |
| R003   | 报告缺少必要章节（如审计意见）         | 高       | 文本中未包含“审计意见”“管理层责任”等关键词 |
| R004   | LLM检测到逻辑不严谨                   | 中       | LLM分析返回“逻辑漏洞”“数据支持不足”   |

#### 自定义规则：
- 新增规则可通过修改`rule_engine.py`实现，或通过配置文件动态加载（需扩展代码）。  


### 3. 本地LLM分析
#### 支持的模型：
- **LLaMA/LLaMA 2**：推荐量化版本（如`ggml-model-q4_0.bin`），支持长上下文（2048 tokens）。  
- **Alpaca-LoRA**：基于LLaMA的指令微调模型，更适合审计场景问答。  
- **ChatGLM-6B**：国产开源模型，支持中文语义理解，推理速度较快。  

#### 分析能力：
1. **逻辑一致性**：检查结论与数据是否匹配（如“收入增长”是否有销量或单价数据支持）。  
2. **合规性**：对比《中国注册会计师审计准则》，识别条款偏离（如未披露关键审计事项）。  
3. **风险识别**：定位潜在风险点（如“关联交易定价不公允”“存货周转率异常下降”）。  


### 4. 数据库管理
#### 存储内容：
- 审计报告元数据（文件路径、名称、上传时间）。  
- 复核结果（规则触发记录、LLM分析文本、整体状态）。  

#### 数据库操作：
- 系统默认使用SQLite（文件`audit_reports.db`），可修改`config.py`切换为PostgreSQL等数据库。  
- 历史记录可通过`database.py`中的接口查询和管理。  


## 七、维护与优化
### 1. 模型性能优化
- **量化模型**：使用更低精度的量化版本（如Q3_K_M），减少内存占用，提升推理速度。  
- **硬件加速**：  
  - CPU：启用AVX2/AVX-512指令集（在`llama.cpp`编译时配置）。  
  - GPU：编译支持CUDA的`llama.cpp`版本，或使用`bitsandbytes`库进行量化训练。  

### 2. 规则与模型迭代
- **新增规则**：在`rule_engine.py`中注册新规则函数，或通过LLM生成规则（如分析历史审计案例自动提取规则）。  
- **模型微调**：使用企业内部审计报告数据微调开源模型，提升特定场景下的分析准确性。  


## 八、常见问题解答
### Q1：OCR识别不准确怎么办？
- A：  
  1. 确保图片清晰，避免倾斜或反光。  
  2. 使用专业OCR工具（如ABBYY FineReader）预处理图片，再导入系统。  
  3. 优先使用电子档报告（PDF/Excel），避免扫描件。  

### Q2：LLM分析速度慢如何解决？
- A：  
  1. 更换更小的模型（如7B参数模型→3B参数模型）。  
  2. 减少上下文窗口大小（`n_ctx`参数，如从2048改为1024）。  
  3. 仅对关键段落调用LLM，而非全文分析。  

### Q3：如何添加自定义审计准则？
- A：  
  1. 在`llm_module.py`中修改Prompt模板，添加新准则条款。  
  2. 例如：  
     ```python
     self.compliance_prompt = PromptTemplate(
         template="检查内容是否符合《中国注册会计师审计准则第X号》：{text}...",
         ...
     )
     ```

