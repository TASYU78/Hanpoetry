# 汉诗语义化开放数据集：唐代与平安朝 (Semantic Framework for Han Poetry: Tang and Heian Open Datasets)

## 简介 (Introduction)

本项目是论文《Toward a Semantic Framework for Han Poetry: Multilingual and Decentralized Integration of East Asian Literary Heritage》中的开放数据集，旨在为学术研究和数据复现提供结构化的历史数据支持。项目包含论文使用到的Demo数据，主要包括唐诗数据库(tang\_db)、平安朝汉诗数据库(heian\_db)和一个小工具包(tools)用于可视化和数据处理。

This project is an open data set from the paper "Toward a Semantic Framework for Han Poetry: Multilingual and Decentralized Integration of East Asian Literary Heritage", aiming to provide structured historical data support for academic research and data reproduction. The project contains demo data used in the paper, including the Tang Poetry Database (tang\_db), the Heian Dynasty Han Poetry Database (heian\_db), and a toolkit (tools) for visualization and data processing.

## 目录 (Table of Contents)

* 简介 (Introduction)
* 项目结构 (Project Structure)
* 数据库说明 (Database Description)
* 工具说明 (Tool Description)
* 使用示例 (Usage Example)

## 项目结构 (Project Structure)

```
项目根目录 (Project Root Directory):
├── Heian_db                 # 平安朝汉诗数据集 (Heian Period Han Poetry Dataset)
│   ├── Ontology             # 本体文件，存储知识图谱 (Ontology files for storing knowledge graphs)
│   │   └── HanpoertyOntology.ttl  # OWL格式文件 (OWL format file)
│   │ 
│   ├── RDF                  # RDF数据 (RDF data)
│   │   ├── Collection.ttl   # 经典诗集 (Classical poetry collection)
│   │   ├── Knowledge.ttl    # 知识数据 (Knowledge data)
│   │   ├── Person.ttl       # 人物数据 (Person data)
│   │   └── Poem.ttl         # 诗歌数据 (Poetry data)
│   ├── SKOS                 # 术语系统 (SKOS vocabularies)
│   │   ├── core.ttl         # 核心术语 (Core vocabulary)
│   │   └── local.ttl        # 本地术语 (Local vocabulary)
│   └── TEI                  # TEI文件 (TEI file)
│       └── nihonsiki.xml    # 日本诗纪TEI文件 (Nihon Shiki TEI file)
│
├── Tang_db                  # 唐代汉诗数据集 (Tang Dynasty Han Poetry Dataset)
│   ├── Ontology             # 本体文件，存储知识图谱 (Ontology files for storing knowledge graphs)
│   │   └── HanpoertyOntology.ttl  # OWL格式文件 (OWL format file)
│   │ 
│   ├── RDF                  # RDF数据 (RDF data)
│   │   ├── Collection.ttl   # 经典诗集 (Classical poetry collection)
│   │   ├── Knowledge.ttl    # 知识数据 (Knowledge data)
│   │   ├── Person.ttl       # 人物数据 (Person data)
│   │   └── Poem.ttl         # 诗歌数据 (Poetry data)
│   ├── SKOS                 # 术语系统 (SKOS vocabularies)
│   │   ├── core.ttl         # 核心术语 (Core vocabulary)
│   │   └── local.ttl        # 本地术语 (Local vocabulary)
│   └── TEI                  # TEI文件 (TEI file)
│       ├── quantangshi.xml  # 全唐诗TEI文件 (Complete Tang Poetry TEI file)
│       └── yingyitangshi.xml    # 英译唐诗精选TEI文件 (Selected Chinese Poems Translated into English Verse TEI file)
│
├── tools                    # 工具 (Tools and visualization scripts)
│   ├── SKOS_viewer.py       # SKOS术语查看器脚本 (SKOS vocabulary viewer script)
│   └── TEI_viewer.html      # TEI格式可视化页面 (TEI format visualization page)
├── README.md                # 项目说明文件 (Project documentation)
└── ReplicationGuide.md      # 论文实验复现指南 (Replication Guide for Paper Experiments)

```

## 数据库说明 (Database Description)

项目中包含两个主要开放数据库，旨在为汉诗研究提供全面数据支持：

The project contains two main open databases aimed at providing comprehensive data support for Han poetry research:

1. **唐代数据库 (Tang\_db)**:

   * 包含唐代汉诗、人物、知识图谱等历史数据。
   * Data format: RDF, OWL, TEI, facilitating data integration and knowledge representation.

2. **平安时代汉诗数据库 (Heian\_db)**:

   * 包含平安时代相关汉诗和人物数据。
   * Data format: RDF, OWL, TEI, consistent with the Tang database.

## 工具说明 (Tool Description)

项目中提供了一些工具脚本，旨在数据预处理和可视化：

The project provides several tool scripts for data preprocessing and visualization:

* **SKOS_viewer.py**:  
  - **功能 (Function)**: 浏览和展示SKOS术语，可用于词汇表和术语体系的可视化。  
  - **使用方法 (Usage)**: 加载项目文件中的 `SKOS` 文件夹下的 `core.ttl` 和 `local.ttl` 文件。  
  - **Purpose**: To browse and visualize SKOS vocabularies, useful for lexicons and terminology systems.  
  - **How to use**: Load the `core.ttl` and `local.ttl` files from the `SKOS` folder in the project.  

* **TEI_viewer.html**:  
  - **功能 (Function)**: 可视化展示TEI格式文档，便于查看和分析TEI格式的汉诗文本。  
  - **使用方法 (Usage)**: 加载项目文件中的 `TEI` 文件夹下的 TEI 文件。  
  - **Purpose**: To visualize TEI format documents for viewing and analyzing Han poetry texts.  
  - **How to use**: Load the TEI files from the `TEI` folder in the project.   

## 补充说明 (Additional Notes)

本项目中的 **ReplicationGuide.md** 文件是为了复现论文实验而提供的详细指南，旨在帮助研究者按照论文中的方法步骤进行实验复刻和验证。  

The **ReplicationGuide.md** file in this project serves as a detailed guide for reproducing the experiments described in the paper, helping researchers follow the methods and steps to replicate and validate the results.
