# 数据复现指南 (Replication Guide)

## 简介 (Introduction)

本文档主要介绍论文《Toward a Semantic Framework for Han Poetry: Multilingual and Decentralized Integration of East Asian Literary Heritage》的复现流程。

The document provides the replication process for the paper "Toward a Semantic Framework for Han Poetry: Multilingual and Decentralized Integration of East Asian Literary Heritage".

论文中使用了开源软件Virtuoso作为数据库，因此在此仅演示如何使用免费版的Virtuoso进行复现。

The paper uses the open-source software Virtuoso as the database. This guide demonstrates how to use the free version of Virtuoso for replication.

## 环境准备 (Environment Setup)

### 1. 数据准备 (Data Preparation)

首先下载并解压本项目中的数据包，得到两个数据集 `Heian_db` 和 `Tang_db`，以及可视化工具包 `tools`。

First, download and extract the data package from this project to obtain the datasets `Heian_db` and `Tang_db`, as well as the visualization toolkit `tools`.

### 2. Virtuoso 设置 (Virtuoso Configuration)

在 Virtuoso 中，分别将 `Heian_db` 和 `Tang_db` 中的 `ttl` 文件上传至以下 URI：

* Heian\_db: `http://hanpoetry.org/heian`
* Tang\_db: `http://hanpoetry.org/tang`

在 Virtuoso 的 SPARQL 端点进行查询。

In Virtuoso, upload the `ttl` files from `Heian_db` and `Tang_db` to the following URIs:

* Heian\_db: `http://hanpoetry.org/heian`
* Tang\_db: `http://hanpoetry.org/tang`

Perform SPARQL queries using the Virtuoso SPARQL endpoint.

> **Note:** 如果希望使用其他查询软件，只需确保将两个数据集分别上传到同一个图 URI 中即可。

> **Note:** If using other query software, just ensure that the datasets are uploaded to the corresponding graph URIs.

## 1. 通过共享知识概念实现跨库检索 (Cross-Database Retrieval via Shared Knowledge Concepts)

### 查询目标 (Query Objective)

检索在唐代与平安时代诗歌库中涉及“月亮”意象的诗歌，检索所有关联至该意象的诗作，并进一步追踪每首诗所关联的主题知识概念,以验证系统在跨库、跨语种语义互通方面的能力。

Retrieve poems involving the imagery of "moon" from both the Tang and Heian poetry databases. Trace the associated thematic knowledge concepts of each poem to evaluate cross-database and cross-linguistic semantic interoperability.

### SPARQL查询 (SPARQL Query)

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX hp: <http://example.org/HanpoetryOWL#>
PREFIX bf: <http://id.loc.gov/ontologies/bibframe/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?dataset ?poem ?titleZh ?titleEn ?themeLabelZh ?themeLabelEn
FROM NAMED <http://hanpoetry.org/tang>
FROM NAMED <http://hanpoetry.org/heian>
WHERE {
  GRAPH ?g {
    ?poem a hp:Poem ;
          bf:title ?titleZh, ?titleEn ;
          hp:hasKnowledge ?knowledge .
    FILTER (lang(?titleZh) = "zh")
    FILTER (lang(?titleEn) = "en")
    FILTER (?knowledge = <http://example.org/hanpoetry/resource/knowledge/ImageryMoon>)
    OPTIONAL {
      ?poem hp:hasKnowledge ?theme .
      ?theme a hp:ThemeConcept .
      OPTIONAL { ?theme rdfs:label ?themeLabelZh . FILTER (lang(?themeLabelZh) = "zh") }
      OPTIONAL { ?theme rdfs:label ?themeLabelEn . FILTER (lang(?themeLabelEn) = "en") }
    }
    BIND(
      IF(STRSTARTS(STR(?g), "http://hanpoetry.org/tang"), "Tang_db",
         IF(STRSTARTS(STR(?g), "http://hanpoetry.org/heian"), "Heian_db", "Unknown")
      ) AS ?dataset
    )
  }
}
ORDER BY ?dataset ?titleZh
```


## 2. 通过Canvas联动TEI资源 (Linking TEI Resources via Canvas)

### 查询目标 (Query Objective)

检索《蜀道难》的TEI编码文本片段及其相关元数据，展示系统将语义实体与多模态资源绑定的能力。

Retrieve TEI-encoded fragments and related metadata of the poem "Shudao Nan" to demonstrate the system's ability to link semantic entities with multimodal resources.


### SPARQL查询 (SPARQL Query)

```sparql
PREFIX bf: <http://id.loc.gov/ontologies/bibframe/>
PREFIX hp: <http://example.org/HanpoetryOWL#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?titleZh ?titleEn ?collectionZh ?collectionEn ?canvas ?tei
FROM <http://hanpoetry.org/tang>
WHERE {
  <http://example.org/hanpoetry/resource/poem/shudaonan> bf:title ?titleZh .
  FILTER (lang(?titleZh) = "zh")
  OPTIONAL { <http://example.org/hanpoetry/resource/poem/shudaonan> bf:title ?titleEn . FILTER (lang(?titleEn) = "en") }
  ?canvas hp:representsPoem <http://example.org/hanpoetry/resource/poem/shudaonan> .
  OPTIONAL { ?canvas hp:hasTEIFragment ?tei . }
  OPTIONAL {
    ?canvas hp:isContainedIn ?range .
    ?range hp:inManifestation ?manifestation .
    ?manifestation hp:isManifestedIn ?collection .
    ?collection rdfs:label ?collectionZh .
    FILTER (lang(?collectionZh) = "zh")
    OPTIONAL { ?collection rdfs:label ?collectionEn . FILTER (lang(?collectionEn) = "en") }
  }
}
```


## 可视化推荐方法 (Recommended Visualization Methods)

为了更好地理解和分析项目数据，我们推荐以下可视化方法：  
To better understand and analyze the project data, we recommend the following visualization methods:  

### 1. 本体可视化 (Ontology Visualization)  
- **推荐工具 (Tool)**: WebVOWL  
- **操作方法 (Usage)**: 使用WebVOWL加载 `ontology.ttl` 文件，查看本体结构。  
  (Use WebVOWL to load the `ontology.ttl` file to view the ontology structure.)  

### 2. SKOS可视化 (SKOS Visualization)  
- **推荐工具 (Tool)**: SKOS_viewer.py (tools文件夹)  
- **操作方法 (Usage)**: 使用脚本读取SKOS文件夹中的 `core.ttl` 和 `local.ttl` 文件。  
  (Use the script to read `core.ttl` and `local.ttl` from the SKOS folder.)  
  ```

