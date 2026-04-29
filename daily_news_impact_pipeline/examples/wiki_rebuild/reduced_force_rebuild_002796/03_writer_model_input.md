SYSTEM PROMPT
You are the writer for a Company Wiki used by downstream agents for company-news matching and impact reasoning.

Your task is to turn the provided source package into one durable, agent-consumable Company Wiki in Simplified Chinese. Write from an investor's analytical perspective: focus on business quality, earnings power, balance-sheet pressure, event sensitivity, and follow-up tracking. Strip away promotional framing in disclosures and research reports; do not write marketing copy or unsupported praise.

First understand the business:
- what the company actually sells, owns, or operates
- who buys from it, who supplies it, and where disclosure is anonymous or incomplete
- where it sits in the value chain and how it monetizes
- what is hard to replicate in product, delivery, certification, manufacturing, channel, data, license, network, or asset base
- which variables drive outcomes and which are only reported results
- which entities, aliases, products, technologies, projects, assets, counterparties, geography, industry terms, and trigger scenarios future news may mention
- what remains unresolved or time-sensitive

Then write a wiki that is useful for both retrieval and reasoning. Identify the underlying operating mechanisms behind the source narrative, but keep factual claims tied to evidence. Prefer concrete mechanisms, named entities, stage wording, and quantitative anchors over generic corporate language. Use the section structure that best fits the source. You may merge sections, rename sections, or omit thin sections.

Coverage contract: when the source package supports it, cover identity surface, business position, quantitative anchors, mechanism or trigger paths, and uncertainty or freshness boundaries. Keep supported names, aliases, products or services, entities, counterparties, assets, projects, geographies, technical terms, customer or supplier concentration, dates, amounts, capacities, operating metrics, and broker-only trigger variables visible for downstream retrieval and impact reasoning.

Use only the provided source package. Treat company filings, annual reports, and announcements as primary sources. Use broker research mainly for research framing, industry vocabulary, trigger variables, and clearly secondary viewpoints. Label broker-only numbers and views explicitly as broker estimates or secondary-source views. When facts conflict or have changed over time, prefer the more recent disclosed source and preserve the relevant date.

Be strict about evidence boundaries. Only state use of proceeds, customers, suppliers, project purposes, capacity, orders, transaction counterparties, transaction status, industry rankings, and future progress when the selected text explicitly provides them. If the source only contains a heading, table stub, empty table, or incomplete excerpt, say that the selected text does not provide the detail. Do not infer the missing rows or details. Factual faithfullness is much more important than making a strong claim. Preserve stage wording such as anonymous customer, sample, validation, small-batch, trial production, under construction, planned, proposed, pending approval, and not disclosed.

USER PROMPT
Company:
世嘉科技 (002796)

How To Read Sources:
Each section lists source files under `Sources`, then selected source text.
Each evidence block starts with `Source: {source_role} | {publish_date} | {doc_family} | {title}`.
`source_role` explains why the file was included.
`publish_date` is the document disclosure/publication date, not necessarily the fiscal period or event date.
`doc_family` is the database document category.
`title` is the original filing/report title.
Use the selected source text as factual evidence. Source titles and section labels are context only.

Source Package:
<<<
# Company Wiki Source Package

## Retrieval Surface
Sources:
- primary_annual_report | 2026-04-26 | annual_report | 2025年年度报告
- origin_document | 2016-04-24 | prospectus | 首次公开发行股票招股说明书
Session:
- session_id: retrieval_surface
- scope: heading=primary_annual_report, origin_document; body=primary_annual_report, origin_document; semantic=none
Selected text:
### Source: primary_annual_report | 2026-04-26 | annual_report | 2025年年度报告
[retrieval=fallback]
一、公司信息
[TABLE p=8 o=28]
header: ["股票简称","世嘉科技","股票代码","002796"]
rows:
["股票上市证券交易所","深圳证券交易所","深圳证券交易所","深圳证券交易所"]
["公司的中文名称","苏州市世嘉科技股份有限公司","苏州市世嘉科技股份有限公司","苏州市世嘉科技股份有限公司"]
["公司的中文简称","世嘉科技","世嘉科技","世嘉科技"]
["公司的外文名称（如有）","Suzhou Shijia Science &Technology Inc.","Suzhou Shijia Science &Technology Inc.","Suzhou Shijia Science &Technology Inc."]
["公司的外文名称缩写（如 有）","SHIJIA TECH","SHIJIA TECH","SHIJIA TECH"]
["公司的法定代表人","王娟","王娟","王娟"]
["注册地址","苏州市建林路 439 号","苏州市建林路 439 号","苏州市建林路 439 号"]
["注册地址的邮政编码","215129","215129","215129"]
["公司注册地址历史变更情况","2023 年 6 月，公司注册地址由'苏州市塘西路 28 号'变更为'苏州市建林路 439 号'。","2023 年 6 月，公司注册地址由'苏州市塘西路 28 号'变更为'苏州市建林路 439 号'。","2023 年 6 月，公司注册地址由'苏州市塘西路 28 号'变更为'苏州市建林路 439 号'。"]
["办公地址","苏州市建林路 439 号","苏州市建林路 439 号","苏州市建林路 439 号"]
["办公地址的邮政编码","215129","215129","215129"]
["公司网址","www.sz-shijia.com","www.sz-shijia.com","www.sz-shijia.com"]
["电子信箱","shijiagufen@shijiakj.com","shijiagufen@shijiakj.com","shijiagufen@shijiakj.com"]
第二节公司简介和主要财务指标
公司年度报告备置地点
四、注册变更情况
[TABLE p=9 o=36]
header: ["统一社会信用代码","913205001379993534"]
["公司上市以来主营业务的变化情况","公司上市之初的主营业务为精密箱体系统的研发、生产及销售，主要产品 为电梯轿厢系统及其他专用设备箱体系统。 2017 年，公司实施了重大资产重组收购了波发特，主营业务增加了滤波 器、基站天线等移动通信设备的研发、生产及销售。 目前，公司主营业务包括移动通信设备业务和精密箱体系统业务。"]
["历次控股股东的变更情况","无变更。"]
五、其他有关资料
[TABLE p=9 o=38]
header: ["会计师事务所名称","容诚会计师事务所（特殊普通合伙）"]
["会计师事务所办公地址","北京市西城区阜成门外大街 22 号 1 幢 10 层 1001-1 至 1001-26"]
["签字会计师姓名","俞国徽、黄冰冰、黄永伟"]

### Source: origin_document | 2016-04-24 | prospectus | 首次公开发行股票招股说明书
[retrieval=fallback]
（一）公司概况
苏州市世嘉科技股份有限公司是由苏州市世嘉科技有限公司整体变更设立的 股份有限公司。 公司于2011年11月2日在江苏省苏州工商行政管理局注册登记， 领取了注册号为 320512000037744 的《企业法人营业执照》 ，注册资本为 6,000 万元。公司住所为苏州市塘西路28号。
一、本次发行基本情况
（1）股票种类：人民币普通股（A股）
（2）股票面值：人民币1.00元
（3）发行股数：本次拟公开发行股票不超过 2,000 万股，不低于发行后总 股本的25%，本次发行全部为新股发行，原股东不公开发售股份
（5）发行市盈率：22.33倍
（6）发行前每股净资产：4.31 元（按照 2015 年 12 月 31 日经审计的归属 于母公司所有者权益除以本次发行前总股本计算）
（7）发行后每股净资产：6.05 元（按照 2015 年 12 月 31 日经审计的净资 产加上本次公开发行新股筹资净额之和除以本次发行后公司总股本计算）
（8）发行市净率：2.14倍（以发行后总股本全面摊薄净资产计算）
（9）发行方式：采用直接定价方式，全部股份通过网上向社会公众投资者 发行，不进行网下询价和配售
（10）发行对象：符合资格的询价对象和在深圳证券交易所开立证券账户的 投资者（国家法律、法规禁止购买者除外）
（11）承销方式：余额包销

## Business And Value Chain
Sources:
- origin_document | 2016-04-24 | prospectus | 首次公开发行股票招股说明书
Session:
- session_id: business_model
- scope: heading=primary_annual_report, origin_document; body=primary_annual_report, origin_document, latest_periodic_like; semantic=primary_annual_report, origin_document, latest_periodic_like
Selected text:
### Source: origin_document | 2016-04-24 | prospectus | 首次公开发行股票招股说明书
[retrieval=heading | chunk_kind=text | expansion=same_heading | heading=（二）主营业务和主要产品 | score=0.8027]
公司是专业的精密箱体系统制造与服务供应商，从事定制化精密箱体系统的 研发、设计、生产、销售以及服务。历经多年发展，公司已经形成包括技术研发、 定制化设计、精密数控加工、表面处理、检验检测、组装配送和技术服务支持在 内的精密箱体系统全流程业务体系，产品广泛应用于电梯制造以及新能源及节能 设备、半导体设备、医疗设备、安检设备、通信设备等专用设备制造领域。
1-1-26

### Source: origin_document | 2016-04-24 | prospectus | 首次公开发行股票招股说明书
[retrieval=heading | chunk_kind=text | expansion=same_heading | heading=（一）发行人主营业务 | score=0.7984]
公司是专业的精密箱体系统制造与服务供应商，从事定制化精密箱体系统的 研发、设计、生产、销售以及服务。历经多年发展，公司已经形成包括技术研发、 定制化设计、精密数控加工、表面处理、检验检测、组装配送和技术服务支持在 内的精密箱体系统全流程业务体系，产品广泛应用于电梯制造以及新能源及节能 设备、半导体设备、医疗设备、安检设备、通信设备等专用设备制造领域。
精密箱体系统是在系统集成设计的基础上，运用现代机械加工的先进工艺方 法对金属或非金属材料进行处理而制成的各类厢体、柜体系统，整个系统需要重 点解决优化材料物理结构、电磁干扰屏蔽、高防护、合理的重量强度比等技术难 题。精密箱体系统的研发涉及结构工程学、结构力学、空气动力学、材料学、电 磁学等多个学科，其设计制造需结合三维设计、逆向工程、仿真模拟、力学测试、 数字参数化及自动化制造等现代技术，故精密箱体系统是一种融合了系统集成设 计与精密制造于一体的产品。

### Source: origin_document | 2016-04-24 | prospectus | 首次公开发行股票招股说明书
[retrieval=heading | chunk_kind=text | expansion=table:full_table | heading=4、销售模式 | score=0.7865]
[TABLE mode=full_table rows=5/5 cols=5]
bridge_before: 发行人产品销售通过与客户协商定价，如需调整价格亦需经双方协商确定。 发行人在与客户协商定价过程中，会根据主要材料成本、 产品的主要增值环节 （包 括：产品研发设计阶段、产品制造阶段和产品技术服务阶段等）以及交货期、信 用期等因素，与客户就产品价格进行综合协商。

发行人结算方式以银行电汇为主，客户的信用期均不超过90天，具体如下：
heading: 4、销售模式
header: ["序号", "客户", "账期", "结算方式", "主要采购产品"]
rows:
["1", "蒂森克虏伯", "蒂森克虏伯中 山公司 45-60 天 蒂森克虏伯上 海公司45天", "电汇", "电梯轿厢整体集成系统"]
["2", "迅达", "45天", "电汇", "电梯轿厢内部集成系统 电梯轿厢整体集成系统"]
["3", "通力", "30-45天", "电汇、银行承 兑汇票", "电梯轿厢整体集成系统"]
["4", "艺达思", "75天", "电汇", "其他专用设备箱体系统"]
["5", "南车", "60天", "银行承兑汇 票、电汇", "新能源及节能设备柜体系统"]

## Customers Suppliers And Entities
Sources:
- origin_document | 2016-04-24 | prospectus | 首次公开发行股票招股说明书
- recent_material_announcement | 2026-01-30 | announcement | 2025年度业绩预告
- recent_material_announcement | 2026-01-12 | announcement | 关于为子公司提供担保事项的进展公告
Session:
- session_id: customers_suppliers_counterparties
- scope: heading=primary_annual_report, origin_document; body=recent_material_announcement; semantic=primary_annual_report, origin_document, recent_material_announcement
Selected text:
### Source: origin_document | 2016-04-24 | prospectus | 首次公开发行股票招股说明书
[retrieval=heading | chunk_kind=table_bridge | expansion=table:full_table | heading=5、报告期前五名客户销售情况 | score=0.7220]
[TABLE mode=full_table rows=5/5 cols=5]
heading: 5、报告期前五名客户销售情况
header: ["期间", "排名", "客户名称", "销售金额（万元）", "占销售收入比重"]
rows:
["", "2", "迅达", "12,962.99", "31.65%"]
["", "3", "通力", "5,062.44", "12.36%"]
["", "4", "艺达思", "1,298.74", "3.17%"]
["", "5", "南车", "499.10", "1.22%"]
["", "合计", "合计", "38,232.32", "93.36%"]
bridge_after: [注]前五大客户销售金额依据同一控制下合并披露

本公司董事、监事、高级管理人员和核心技术人员，主要关联方或持有本公 司5%以上股份的股东， 在前五名客户中不拥有任何权益， 亦不存在任何关联关系。

### Source: origin_document | 2016-04-24 | prospectus | 首次公开发行股票招股说明书
[retrieval=heading | chunk_kind=table_bridge | expansion=table:full_table | heading=5、报告期前五名客户销售情况 | score=0.7220]
[TABLE mode=full_table rows=13/13 cols=5]
heading: 5、报告期前五名客户销售情况
header: ["期间", "排名", "客户名称", "销售金额（万元）", "占销售收入比重"]
rows:
["2015年度", "1", "蒂森克虏伯", "18,098.26", "39.14%"]
["2015年度", "2", "迅达", "13,627.91", "29.47%"]
["2015年度", "3", "通力", "7,489.43", "16.20%"]
["2015年度", "4", "金峰", "976.18", "2.11%"]
["2015年度", "5", "赛默飞世尔", "944.42", "2.04%"]
["2015年度", "合计", "合计", "41,136.19", "88.96%"]
["2014年度", "1", "蒂森克虏伯", "20,562.70", "46.39%"]
["2014年度", "2", "迅达", "13,419.08", "30.27%"]
["2014年度", "3", "通力", "5,865.81", "13.23%"]
["2014年度", "4", "艺达思", "1,067.71", "2.41%"]
["2014年度", "5", "南车", "488.03", "1.10%"]
["2014年度", "合计", "合计", "41,403.33", "93.41%"]
["2013年度", "1", "蒂森克虏伯", "18,409.06", "44.95%"]
bridge_after: [注]前五大客户销售金额依据同一控制下合并披露

本公司董事、监事、高级管理人员和核心技术人员，主要关联方或持有本公 司5%以上股份的股东， 在前五名客户中不拥有任何权益， 亦不存在任何关联关系。

### Source: origin_document | 2016-04-24 | prospectus | 首次公开发行股票招股说明书
[retrieval=heading | chunk_kind=table_row | expansion=table:full_table | heading=（三）报告期内公司向前五名供应商采购情况 | score=0.6624]
[TABLE mode=full_table rows=1/1 cols=6]
heading: （三）报告期内公司向前五名供应商采购情况
header: ["col_1", "col_2", "col_3", "col_4", "col_5", "col_6"]
rows:
["期间", "序 号", "供应商名称", "主要采购产品", "采购金额 （万元）", "占当年采购 金额比重"]
bridge_after: 报告期内，公司不存在采购金额占比超过 50%的单个供应商。除世嘉新精密 以外，本公司董事、监事、高级管理人员和核心技术人员，主要关联方或持有本 公司5%以上股份的股东，在上述供应商中不拥有任何权益，亦不存在任何关联关 系。

### Source: origin_document | 2016-04-24 | prospectus | 首次公开发行股票招股说明书
[retrieval=heading | chunk_kind=table_row | expansion=table:full_table | heading=（三）报告期内公司向前五名供应商采购情况 | score=0.6619]
[TABLE mode=full_table rows=18/18 cols=6]
heading: （三）报告期内公司向前五名供应商采购情况
header: ["期间", "序 号", "供应商名称", "主要采购产品", "采购金额 （万元）", "占当年采购 金额比重"]
rows:
["年度", "1", "海门市森达装饰材料有限公司", "不锈钢板", "2,465.51", "8.15%"]
["年度", "2", "苏州市昊淇精密钣金有限公司", "外购钣金件", "1,020.66", "3.38%"]
["年度", "3", "吴江市莘塔恒丰五金塑料制品厂", "外购钣金件", "1,018.34", "3.37%"]
["年度", "4", "苏州德道通快激光钣金有限公司", "外购钣金件", "984.54", "3.26%"]
["年度", "5", "苏州涌协精密机械有限公司", "外购钣金件", "812.46", "2.69%"]
["年度", "合计", "合计", "合计", "6,301.51", "20.85%"]
["2014 年度", "1", "江苏华力金属材料有限公司", "不锈钢板", "1,858.62", "6.37%"]
["2014 年度", "2", "吴江市莘塔恒丰五金塑料制品厂", "外购钣金件", "1,681.85", "5.77%"]
["2014 年度", "3", "苏州市昊淇精密钣金有限公司", "外购钣金件", "1,261.94", "4.33%"]
["2014 年度", "4", "海门市森达装饰材料有限公司", "不锈钢板", "1,198.35", "4.11%"]
["2014 年度", "5", "扬州尼尔工程塑料有限公司", "外购轿顶轮组件", "960.72", "3.29%"]
["2014 年度", "合计", "合计", "合计", "6,961.48", "23.87%"]
["2013 年度", "1", "海门市森达装饰材料有限公司", "不锈钢板", "2,113.62", "7.78%"]
["2013 年度", "2", "吴江市莘塔恒丰五金塑料制品厂", "外购钣金件", "2,032.08", "7.48%"]
["2013 年度", "3", "苏州市昊淇精密钣金有限公司", "外购钣金件", "1,335.23", "4.91%"]
["2013 年度", "4", "上海恒亿实业有限公司", "钢板", "1,210.56", "4.45%"]
["2013 年度", "5", "扬州尼尔工程塑料有限公司", "外购轿顶轮组件", "1,167.71", "4.30%"]
["2013 年度", "合计", "合计", "合计", "7,859.20", "28.92%"]
bridge_after: 报告期内，公司不存在采购金额占比超过 50%的单个供应商。除世嘉新精密 以外，本公司董事、监事、高级管理人员和核心技术人员，主要关联方或持有本 公司5%以上股份的股东，在上述供应商中不拥有任何权益，亦不存在任何关联关 系。

### Source: recent_material_announcement | 2026-01-30 | announcement | 2025年度业绩预告
[retrieval=body | chunk_kind=table_row | expansion=table:full_table | heading=一、本期业绩预计情况 | score=0.8115]
[TABLE mode=full_table rows=5/5 cols=3]
bridge_before: □同向上升

□同向下降
heading: 一、本期业绩预计情况
header: ["项 目", "本报告期", "上年同期"]
rows:
["归属于上市公司股东的净 利润", "亏损： 4,900.00 万元- 5,900.00 万元", "盈利： 9,212.33 万元"]
["归属于上市公司股东的扣 除非经常性损益的净利润", "亏损： 5,900.00 万元- 6,900.00 万元", "亏损： 1,289.90 万元"]
["营业收入", "91,000.00 万元- 98,000.00 万元", "95,951.49 万元"]
["扣除后营业收入 [ 注 1]", "89,000.00 万元- 96,000.00 万元", "93,327.79 万元"]
["基本每股收益", "亏损： 0.20 元 / 股- 0.24 元 / 股", "盈利： 0.37 元 / 股"]
bridge_after: 注 1 ：扣除后营业收入指扣除与主营业务无关的业务收入和不具备商业实质的收入后的 营业收入。

### Source: recent_material_announcement | 2026-01-12 | announcement | 关于为子公司提供担保事项的进展公告
[retrieval=body | chunk_kind=text | expansion=same_chunk | heading=二、担保进展情况 | score=0.7283]
近日，公司全资子公司苏州波发特电子科技有限公司（以下简称'波发特' ） 向上海银行股份有限公司苏州分行（以下简称'上海银行'）申请了 5,000.00 万 元的综合授信业务， 公司将在此授信额度内为波发特提供 5,000.00 万元的连带责 任担保，并与上海银行签署《最高额保证合同》（合同编号： ZDB308251659 ）， 保证合同主要内容如下：
债权人：上海银行股份有限公司苏州分行。
2.
保证方式：连带责任保证。
担保的最高主债权限额：主债权余额最高不超过人民币 5,000 万元。
主债权余额 = 已经发生的主债权累计额 -已经偿还的主债权累计额。
若主债权为本外币混用的授信，则主债权最高余额系指等值人民币余额。
保证担保的范围：主债权所达的债权本金、利息、罚息、违约金、赔偿 金以及主合同项下应缴未缴的保证金；与主债权有关的所有银行费用（包括但不 限于开证手续费、信用证修改费、提单背书费、承兑费、托收手续费、风险承担 费）；债权及 / 或担保物权实现费用（包括但不限于催收费用、诉讼费用、保全 费、执行费、律师费、担保物处置费、公告费、拍卖费、过户费、差旅费等）以 及债务人给债权人造成的其他损失。

### Source: recent_material_announcement | 2026-01-12 | announcement | 关于为子公司提供担保事项的进展公告
[retrieval=body | chunk_kind=text | expansion=same_chunk | heading=三、累计对外担保数量及逾期担保数量 | score=0.7090]
截至本公告披露日， 公司及其控股子公司与业务相关方签署的担保协议金额 合计人民币 35,100.00 万元，占公司最近一期经审计归属于母公司所有者权益的
38.80% ，占公司最近一期经审计总资产的 24.01% ；公司及其控股子公司的担保 余额合计人民币 11,556.14 万元，占公司最近一期经审计的归属于母公司所有者 权益的 12.77% ，占公司最近一期经审计总资产的 7.91% ；公司及其控股子公司 未发生违规担保和逾期担保的情形。

### Source: recent_material_announcement | 2026-01-30 | announcement | 2025年度业绩预告
[retrieval=body | chunk_kind=text | expansion=same_chunk | heading=三、业绩变动原因说明 | score=0.6949]
报告期内，公司经营业绩出现亏损主要系：一是报告期内，公司部分产品面 临激烈的市场竞争，产品毛利率下降；二是报告期内，子公司中山亿泰纳因临时 停产发生的相关费用增加；三是本期股权激励费用较上期增加。
报告期内，非经常性损益对归属于上市公司股东净利润的影响金额约为 970 万元，主要系本期公司持有的荣旗科技股份确认的公允价值变动收益、减持荣旗 科技股份确认的投资收益及投资重元贰号基金确认的投资收益。

## Financial And Segment Anchors
Sources:
- primary_annual_report | 2026-04-26 | annual_report | 2025年年度报告
- latest_periodic_like | 2026-04-26 | announcement | 2026年一季度报告
Session:
- session_id: financial_segments_quality
- scope: heading=primary_annual_report, latest_periodic_like; body=primary_annual_report, latest_periodic_like; semantic=primary_annual_report, latest_periodic_like
Selected text:
### Source: primary_annual_report | 2026-04-26 | annual_report | 2025年年度报告
[retrieval=fallback]
六、主要会计数据和财务指标
1 、公司无需追溯调整或重述以前年度会计数据
[TABLE p=9 o=41]
header: ["项目","2025 年","2024 年","本年比上年 增减","2023 年"]
rows:
["营业收入（元）","944,662,412.61","959,514,901.87","-1.55%","1,048,007,534.50"]
["归属于上市公司股东的净利润 （元）","-56,547,967.16","92,123,324.94","-161.38%","-14,689,489.27"]
["归属于上市公司股东的扣除非经 常性损益的净利润（元）","-66,496,572.61","-12,898,988.89","-415.52%","-27,508,867.49"]
["经营活动产生的现金流量净额 （元）","20,306,501.92","-6,669,230.14","404.48%","84,101,477.62"]
["基本每股收益（元 / 股）","-0.23","0.37","-162.16%","-0.06"]
["稀释每股收益（元 / 股）","-0.23","0.37","-162.16%","-0.06"]
["加权平均净资产收益率","-6.46%","10.47%","-16.93%","0.00%"]
["项目","2025 年末","2024 年末","本年末比上 年末增减","2023 年末"]
["总资产（元）","1,562,111,814.38","1,461,612,626.40","6.88%","1,461,832,418.93"]
["归属于上市公司股东的净资产 （元）","862,914,702.79","904,603,820.96","-4.61%","853,825,710.55"]
2 、公司最近三个会计年度扣除非经常性损益前后净利润孰低者均为负值，且最近一年审计 报告显示公司持续经营能力存在不确定性：否。
3 、营业收入扣除情况
江苏省苏州市虎丘区建林路 439 号世嘉科技证券部
[TABLE p=10 o=45]
header: ["项目","2025 年","2024 年","备注"]
["营业收入（元）","944,662,412.61","959,514,901.87","如下所示"]
["营业收入扣除金额（元）","23,826,210.09","26,237,007.80","与主营业务无关的收入"]
["营业收入扣除后金额（元）","920,836,202.52","933,277,894.07","扣除与主营业务无关后的收入"]
八、分季度主要财务指标
[TABLE p=10 o=52]
header: ["项目","第一季度","第二季度","第三季度","第四季度"]
["营业收入","178,360,395.36","232,500,594.97","262,945,702.48","270,855,719.80"]
["归属于上市公司股东的净利润","-18,795,743.31","-25,812,842.08","-6,406,240.43","-5,533,141.34"]
["归属于上市公司股东的扣除非 经常性损益的净利润","-14,574,862.81","-18,430,576.72","-25,297,375.87","-8,193,757.21"]
["经营活动产生的现金流量净额","-26,257,365.94","64,525,635.74","-24,947,141.99","6,985,374.11"]
单位：元
上述财务指标或其加总数与公司已披露季度报告、半年度报告相关财务指标不存在重大差异。
（ 1 ）营业收入构成
[TABLE p=19 o=138]
header: ["项目","2025 年","2025 年","2024 年","2024 年","同比增减"]
["项目","金额","占营业收入 比重","金额","占营业收入 比重","同比增减"]
["营业收入合计","944,662,412.61","100%","959,514,901.87","100%","-1.55%"]

### Source: latest_periodic_like | 2026-04-26 | announcement | 2026年一季度报告
[retrieval=fallback]
一、主要财务数据
（一）主要会计数据和财务指标
公司无需追溯调整或重述以前年度会计数据。
[TABLE p=2 o=14]
header: ["项目","本报告期","上年同期","本报告期比上年同期 增减"]
rows:
["营业收入（元）","192,708,903.80","178,360,395.36","8.04%"]
["归属于上市公司股东的净利润（元）","-23,491,827.61","-18,795,743.31","-24.98%"]
["归属于上市公司股东的扣除非经常性损益 的净利润（元）","-22,808,811.48","-14,574,862.81","-56.49%"]
["经营活动产生的现金流量净额（元）","-31,162,167.46","-26,257,365.94","-18.68%"]
["基本每股收益（元 / 股）","-0.09","-0.08","-12.50%"]
["稀释每股收益（元 / 股）","-0.09","-0.08","-12.50%"]
["加权平均净资产收益率","-2.76%","-2.11%","-0.65%"]
["项目","本报告期末","上年度末","本报告期末比上年度 末增减"]
["总资产（元）","1,560,054,108.94","1,562,111,814.38","-0.13%"]
["归属于上市公司股东的所有者权益（元）","842,453,193.27","862,914,702.79","-2.37%"]
[TABLE p=2 o=16]
header: ["项目","本报告期金额","说明"]
["非流动性资产处置损益（包括已计提资产减值准备的冲销部分）","-110,171.98",""]
["计入当期损益的政府补助（与公司正常经营业务密切相关、符合 国家政策规定、按照确定的标准享有、对公司损益产生持续影响 的政府补助除外）","405,652.11","主要系本期收到的政府 补助。"]
["除同公司正常经营业务相关的有效套期保值业务外，非金融企业 持有金融资产和金融负债产生的公允价值变动损益以及处置金融 资产和金融负债产生的损益","-883,374.88","主要系本期持有荣旗科 技股票产生的公允价值 变动收益。"]
["除上述各项之外的其他营业外收入和支出","-95,121.38",""]
["合计","-683,016.13","--"]
单位：元
公司不存在其他符合非经常性损益定义的损益项目的具体情况。
公司不存在将《公开发行证券的公司信息披露解释性公告第 1 号--非经常性损益》中列举的非经 常性损益项目界定为经常性损益的项目的情形。
（三）主要会计数据和财务指标发生变动的情况及原因
[TABLE p=3 o=22]
header: ["项目","期末余额 / 本期发生额","年初余额 / 上期发生额","变动比例","变动原因"]
["货币资金","157,561,735.95","261,156,020.22","-39.67%","主要系本期归还短期借款以及 支付光彩芯辰投资款所致。"]
["应收账款融资","6,851,479.45","39,009,451.47","-82.44%","主要系本期子公司波发特收到 的银行承兑汇票减少所致。"]
["其他流动资产","2,410,220.03","3,497,511.37","-31.09%","主要系本期孙公司恩电开增值 税借方余额重分类减少所致。"]
["长期股权投资","278,486,634.12","61,794.65","450564.64%","主要系本期光彩芯辰投资款增 加所致。"]
["其他非流动资产","1,341,210.00","121,227,225.62","-98.89%","主要系本期光彩芯辰预付投资 款转长期股权投资所致。"]
["短期借款","71,839,382.98","136,064,144.94","-47.20%","主要系本期归还短期借款较多 以及子公司商票贴现到期冲减 所致。"]
["应交税费","2,758,939.26","1,714,288.44","60.94%","主要系本期公司应交增值税增 加所致。"]
["一年内到期的非流动负债","26,816,071.80","7,569,572.36","254.26%","主要系本期一年内到期的长期 借款增加所致。"]
["其他流动负债","134,222.06","17,828,231.67","-99.25%","主要系本期已背书未到期票据 减少所致。"]
["长期借款","210,271,140.00","57,401,140.00","266.32%","主要系本期长期借款增加所 致。"]
["财务费用","3,478,177.74","121,072.66","2772.80%","主要系本期借款利息支出增加 及受美元汇率影响汇兑损失增 加所致。"]
["其他收益","757,101.73","1,165,498.18","-35.04%","主要系本期享受先进制造业进 项税加计抵减额减少所致。"]

## Operating Assets Projects And Capacity
Sources:
- recent_material_announcement | 2026-01-30 | announcement | 2025年度业绩预告
- recent_material_announcement | 2026-02-02 | announcement | 关于对外投资的进展公告
- recent_material_announcement | 2026-01-12 | announcement | 关于为子公司提供担保事项的进展公告
Session:
- session_id: products_assets_projects
- scope: heading=primary_annual_report, latest_periodic_like; body=recent_material_announcement; semantic=primary_annual_report, latest_periodic_like, recent_material_announcement
Selected text:
### Source: recent_material_announcement | 2026-01-30 | announcement | 2025年度业绩预告
[retrieval=body | chunk_kind=text | expansion=table:full_table | heading=一、本期业绩预计情况 | score=0.6808]
[TABLE mode=full_table rows=5/5 cols=3]
bridge_before: □同向上升

□同向下降
heading: 一、本期业绩预计情况
header: ["项 目", "本报告期", "上年同期"]
rows:
["归属于上市公司股东的净 利润", "亏损： 4,900.00 万元- 5,900.00 万元", "盈利： 9,212.33 万元"]
["归属于上市公司股东的扣 除非经常性损益的净利润", "亏损： 5,900.00 万元- 6,900.00 万元", "亏损： 1,289.90 万元"]
["营业收入", "91,000.00 万元- 98,000.00 万元", "95,951.49 万元"]
["扣除后营业收入 [ 注 1]", "89,000.00 万元- 96,000.00 万元", "93,327.79 万元"]
["基本每股收益", "亏损： 0.20 元 / 股- 0.24 元 / 股", "盈利： 0.37 元 / 股"]
bridge_after: 注 1 ：扣除后营业收入指扣除与主营业务无关的业务收入和不具备商业实质的收入后的 营业收入。

### Source: recent_material_announcement | 2026-02-02 | announcement | 关于对外投资的进展公告
[retrieval=body | chunk_kind=text | expansion=neighbor_window | heading=二、交易进展情况 | score=0.6557]
2025 年 12 月 26 日，苏州市世嘉科技股份有限公司（以下简称'公司'或 者'世嘉科技'）召开第五届董事会第十二次会议，审议通过了《关于签署 < 苏 州市世嘉科技股份有限公司关于光彩芯辰（浙江）科技有限公司之投资协议 > 与 < 关于光彩芯辰（浙江）科技有限公司之 B5 轮股东协议 > 的议案》，即：公司拟 通过增资扩股及受让标的公司创始股东部分股权方式取得光彩芯辰（浙江）科技 有限公司（以下简称'标的公司'）共计 20% 股权。本次交易对价为 2.75 亿元， 本次交易完成后本公司持有标的公司共计 20% 的股权（以下简称'本次交易'） ， 具体内容详见公司于 2025 年 12 月 30 日在指定信息披露媒体上披露的《关于对 外投资的公告》（公告编号： 2025-072 ）。
2026 年 1 月 14 日，公司在指定信息披露媒体上披露了《关于对外投资的进 展公告》 （公告编号： 2026-009 ），即公司已向标的公司支付了增资款 1.20 亿元， 同时标的公司已完成相应股权的变更登记。

### Source: recent_material_announcement | 2026-01-30 | announcement | 2025年度业绩预告
[retrieval=body | chunk_kind=text | expansion=same_chunk | heading=三、业绩变动原因说明 | score=0.6448]
报告期内，公司经营业绩出现亏损主要系：一是报告期内，公司部分产品面 临激烈的市场竞争，产品毛利率下降；二是报告期内，子公司中山亿泰纳因临时 停产发生的相关费用增加；三是本期股权激励费用较上期增加。
报告期内，非经常性损益对归属于上市公司股东净利润的影响金额约为 970 万元，主要系本期公司持有的荣旗科技股份确认的公允价值变动收益、减持荣旗 科技股份确认的投资收益及投资重元贰号基金确认的投资收益。

### Source: recent_material_announcement | 2026-01-12 | announcement | 关于为子公司提供担保事项的进展公告
[retrieval=body | chunk_kind=text | expansion=same_chunk | heading=三、累计对外担保数量及逾期担保数量 | score=0.5758]
截至本公告披露日， 公司及其控股子公司与业务相关方签署的担保协议金额 合计人民币 35,100.00 万元，占公司最近一期经审计归属于母公司所有者权益的
38.80% ，占公司最近一期经审计总资产的 24.01% ；公司及其控股子公司的担保 余额合计人民币 11,556.14 万元，占公司最近一期经审计的归属于母公司所有者 权益的 12.77% ，占公司最近一期经审计总资产的 7.91% ；公司及其控股子公司 未发生违规担保和逾期担保的情形。

### Source: recent_material_announcement | 2026-01-12 | announcement | 关于为子公司提供担保事项的进展公告
[retrieval=body | chunk_kind=text | expansion=same_chunk | heading=二、担保进展情况 | score=0.5725]
近日，公司全资子公司苏州波发特电子科技有限公司（以下简称'波发特' ） 向上海银行股份有限公司苏州分行（以下简称'上海银行'）申请了 5,000.00 万 元的综合授信业务， 公司将在此授信额度内为波发特提供 5,000.00 万元的连带责 任担保，并与上海银行签署《最高额保证合同》（合同编号： ZDB308251659 ）， 保证合同主要内容如下：
债权人：上海银行股份有限公司苏州分行。
2.
保证方式：连带责任保证。
担保的最高主债权限额：主债权余额最高不超过人民币 5,000 万元。
主债权余额 = 已经发生的主债权累计额 -已经偿还的主债权累计额。
若主债权为本外币混用的授信，则主债权最高余额系指等值人民币余额。
保证担保的范围：主债权所达的债权本金、利息、罚息、违约金、赔偿 金以及主合同项下应缴未缴的保证金；与主债权有关的所有银行费用（包括但不 限于开证手续费、信用证修改费、提单背书费、承兑费、托收手续费、风险承担 费）；债权及 / 或担保物权实现费用（包括但不限于催收费用、诉讼费用、保全 费、执行费、律师费、担保物处置费、公告费、拍卖费、过户费、差旅费等）以 及债务人给债权人造成的其他损失。

## Capital Transactions And Obligations
Sources:
- recent_material_announcement | 2026-01-30 | announcement | 2025年度业绩预告
- recent_material_announcement | 2026-01-12 | announcement | 关于为子公司提供担保事项的进展公告
- recent_material_announcement | 2026-02-02 | announcement | 关于对外投资的进展公告
Session:
- session_id: capital_obligations
- scope: heading=primary_annual_report, latest_periodic_like; body=recent_material_announcement; semantic=primary_annual_report, latest_periodic_like, recent_material_announcement
Selected text:
### Source: recent_material_announcement | 2026-01-30 | announcement | 2025年度业绩预告
[retrieval=body | chunk_kind=table_row | expansion=table:full_table | heading=一、本期业绩预计情况 | score=0.7590]
[TABLE mode=full_table rows=5/5 cols=3]
bridge_before: □同向上升

□同向下降
heading: 一、本期业绩预计情况
header: ["项 目", "本报告期", "上年同期"]
rows:
["归属于上市公司股东的净 利润", "亏损： 4,900.00 万元- 5,900.00 万元", "盈利： 9,212.33 万元"]
["归属于上市公司股东的扣 除非经常性损益的净利润", "亏损： 5,900.00 万元- 6,900.00 万元", "亏损： 1,289.90 万元"]
["营业收入", "91,000.00 万元- 98,000.00 万元", "95,951.49 万元"]
["扣除后营业收入 [ 注 1]", "89,000.00 万元- 96,000.00 万元", "93,327.79 万元"]
["基本每股收益", "亏损： 0.20 元 / 股- 0.24 元 / 股", "盈利： 0.37 元 / 股"]
bridge_after: 注 1 ：扣除后营业收入指扣除与主营业务无关的业务收入和不具备商业实质的收入后的 营业收入。

### Source: recent_material_announcement | 2026-01-12 | announcement | 关于为子公司提供担保事项的进展公告
[retrieval=body | chunk_kind=text | expansion=same_chunk | heading=二、担保进展情况 | score=0.7358]
近日，公司全资子公司苏州波发特电子科技有限公司（以下简称'波发特' ） 向上海银行股份有限公司苏州分行（以下简称'上海银行'）申请了 5,000.00 万 元的综合授信业务， 公司将在此授信额度内为波发特提供 5,000.00 万元的连带责 任担保，并与上海银行签署《最高额保证合同》（合同编号： ZDB308251659 ）， 保证合同主要内容如下：
债权人：上海银行股份有限公司苏州分行。
2.
保证方式：连带责任保证。
担保的最高主债权限额：主债权余额最高不超过人民币 5,000 万元。
主债权余额 = 已经发生的主债权累计额 -已经偿还的主债权累计额。
若主债权为本外币混用的授信，则主债权最高余额系指等值人民币余额。
保证担保的范围：主债权所达的债权本金、利息、罚息、违约金、赔偿 金以及主合同项下应缴未缴的保证金；与主债权有关的所有银行费用（包括但不 限于开证手续费、信用证修改费、提单背书费、承兑费、托收手续费、风险承担 费）；债权及 / 或担保物权实现费用（包括但不限于催收费用、诉讼费用、保全 费、执行费、律师费、担保物处置费、公告费、拍卖费、过户费、差旅费等）以 及债务人给债权人造成的其他损失。

### Source: recent_material_announcement | 2026-01-12 | announcement | 关于为子公司提供担保事项的进展公告
[retrieval=body | chunk_kind=text | expansion=same_chunk | heading=三、累计对外担保数量及逾期担保数量 | score=0.7053]
截至本公告披露日， 公司及其控股子公司与业务相关方签署的担保协议金额 合计人民币 35,100.00 万元，占公司最近一期经审计归属于母公司所有者权益的
38.80% ，占公司最近一期经审计总资产的 24.01% ；公司及其控股子公司的担保 余额合计人民币 11,556.14 万元，占公司最近一期经审计的归属于母公司所有者 权益的 12.77% ，占公司最近一期经审计总资产的 7.91% ；公司及其控股子公司 未发生违规担保和逾期担保的情形。

### Source: recent_material_announcement | 2026-02-02 | announcement | 关于对外投资的进展公告
[retrieval=body | chunk_kind=text | expansion=neighbor_window | heading=二、交易进展情况 | score=0.6575]
2025 年 12 月 26 日，苏州市世嘉科技股份有限公司（以下简称'公司'或 者'世嘉科技'）召开第五届董事会第十二次会议，审议通过了《关于签署 < 苏 州市世嘉科技股份有限公司关于光彩芯辰（浙江）科技有限公司之投资协议 > 与 < 关于光彩芯辰（浙江）科技有限公司之 B5 轮股东协议 > 的议案》，即：公司拟 通过增资扩股及受让标的公司创始股东部分股权方式取得光彩芯辰（浙江）科技 有限公司（以下简称'标的公司'）共计 20% 股权。本次交易对价为 2.75 亿元， 本次交易完成后本公司持有标的公司共计 20% 的股权（以下简称'本次交易'） ， 具体内容详见公司于 2025 年 12 月 30 日在指定信息披露媒体上披露的《关于对 外投资的公告》（公告编号： 2025-072 ）。
2026 年 1 月 14 日，公司在指定信息披露媒体上披露了《关于对外投资的进 展公告》 （公告编号： 2026-009 ），即公司已向标的公司支付了增资款 1.20 亿元， 同时标的公司已完成相应股权的变更登记。

## Industry Competition And Trigger Context
Sources:
- origin_document | 2016-04-24 | prospectus | 首次公开发行股票招股说明书
Session:
- session_id: industry_competition_triggers
- scope: heading=primary_annual_report, origin_document; body=primary_annual_report, origin_document, secondary_research_context; semantic=primary_annual_report, origin_document, secondary_research_context
Selected text:
### Source: origin_document | 2016-04-24 | prospectus | 首次公开发行股票招股说明书
[retrieval=heading | chunk_kind=text | expansion=same_heading | heading=（一）行业竞争格局 | score=0.6723]
精密箱体系统制造行业涉及的下游行业众多，随着各行业技术进步，下游需 求细分层次性日益显著。市场呈现出高度细分化的'蜂窝格局' ，且各'蜂窝'都 有着可观的发展潜力。
精密箱体系统制造行业的'蜂窝格局'
在庞大的市场容量下，根据下游行业产品功能、特点、使用目的及应用领域 的不同，本行业产品具有细分化特点，各细分市场间对于精密箱体系统产品的技
术要求存在差异：电梯制造领域主要关注轿厢系统与其他系统部件的契合度及自 身重量；专用设备制造领域主要考察产品在面对恶劣户外环境时，对内部元器件 的保护程度和内部的电磁防干扰水平以及箱体系统内部结构设计的精密度。
虽然各细分市场相对独立，但其之间亦存在共性：各细分市场前景广阔，单 个领域均可深耕，在单独'蜂窝'内形成规模化生产和品牌化效应后，一定程度 上可遏制潜在进入者，降低该领域内的竞争程度；另外，细分行业内研发设计能 力较强、生产制造经验丰富的优质企业的业务往往会涉足其他领域，在多'蜂窝' 全面发展。

### Source: origin_document | 2016-04-24 | prospectus | 首次公开发行股票招股说明书
[retrieval=heading | chunk_kind=text | expansion=same_heading | heading=1、行业发展的有利因素 | score=0.6642]
（1）政策鼓励与支持为本行业带来良好的政策环境
国家政策的支持将给精密箱体系统行业带来长期的鼓励与支持，国家先后出 台《国家中长期科学和技术发展规划纲要（2006-2020 年） 》 、 《中华人民共和国国 民经济和社会发展第十二个五年规划纲要》 、 《工业转型升级规划（2011-2015 年） 》 、 《高端装备制造业'十二五'发展规划》等产业振兴政策，提出要优化产业 结构、加大高端装备制造业发展力度、增强产业配套能力、尤其是重点研究开发 关键基础件和通用部件的设计，提高我国高端装备所需的关键配套系统与设备、 关键零部件与基础件制造能力、基础配套能力。
针对本行业服务的电梯制造行业，2013年出台的《中华人民共和国特种设备 安全法》规定包括电梯在内的特种设备存在严重事故隐患，无改造、维修价值， 或者超过安全技术规范规定的其他报废条件，例如使用年限等，特种设备使用单 位应当及时予以报废。2012年建设部出台的《住宅设计规范》GB50096-2011，规 定12 层及 12 层以上的住宅，每栋楼设置电梯不应少于两台，并将原《规范》中 '宜'设置一台可容纳担架的电梯，修改为'应'设置一台可容纳担架的电梯，
使其成为强制标准。
针对本行业服务的新能源及节能设备制造业，国家先后出台《可再生能源发 展'十二五'规划》 、 《太阳能发电科技发展'十二五'专项规划》 、 《风力发电科 技发展'十二五'专项规划》 、 《 '十二五'节能环保产业发展规划》等鼓励政策提
振专用设备的发展。
（2）产品应用领域的日益拓展为行业创造了巨大的新增市场
随着我国经济建设的快速发展和城镇化建设的加速，商业地产、城市基础设 施建设、保障房建设、旧电梯更新及旧楼改造均对电梯产生了巨大需求；而变频 器、风电变流器、光伏逆变器等新能源与节能专用设备行业的迅速发展已成为精 密箱体系统行业新的利润增长点；此外，半导体、轨道交通、通信、医疗、航空 航天等高端专用设备制造将为精密箱体系统市场的发展带来新的机遇与增量空 间。
（3）定制化发展趋势增强整机制造与配套厂商的分工、合作关系
精密箱体系统产品具有非常明显的定制化特点，例如电梯制造领域不同建筑 物及客户对电梯的材料、装饰、规格、性能指标往往有不同的要求，而专用设备 领域对各种柜体均有不同的规格、型号、性能的要求。在经济全球化的大潮推动 下，越来越多的整机制造商为集中精力强化自己的核心竞争力、拓展业务范围， 而选择将部件制造业务外协给专业的供应商， 通过总装集成方式生产其品牌产品。 因此，采用向专业配套厂商外购或外协零部件的模式已成为整机制造商发展的基 本模式，整机制造商和配套厂商通过明确的分工体系形成了紧密的合作关系，并 且通过专业化生产有效地提升了整个行业的生产效率和产品质量。所以，整机制 造商与配套厂商专业化分工的趋势将为精密箱体系统行业的发展带来更为广阔的 市场空间。
（4）高、精、尖产业向中国转移为行业发展带来了新的发展机遇
随着'世界工厂'地位的确立，我国逐渐由制造大国向制造强国转变，国内 企业技术水平也稳步提升。国际厂商已越来越多采用国内品质优良且价格合理的 系统组件配套其最终产品，以进一步提升其在全球市场的产品竞争力。以电梯制 造企业为例，为抢占全球最大、最具潜力的中国市场，迅达、蒂森克虏伯、通力、
奥的斯等国际知名电梯制造巨头出于降低成本及接近目标市场等考虑，纷纷在中
国建立了生产基地和全球采购平台。

### Source: origin_document | 2016-04-24 | prospectus | 首次公开发行股票招股说明书
[retrieval=heading | chunk_kind=text | expansion=same_heading | heading=（三）行业发展现状与前景 | score=0.6484]
伴随我国精密箱体制造行业的不断发展，本行业产品广泛应用于电梯制造以 及新能源及节能设备、半导体设备、医疗设备、轨道交通设备、通信设备、航空 航天等专用设备制造领域，发展前景和机遇良好。

### Source: origin_document | 2016-04-24 | prospectus | 首次公开发行股票招股说明书
[retrieval=heading | chunk_kind=text | expansion=same_heading | heading=（1）下游行业发展情况 | score=0.6472]
公司目前主营业务收入主要来源于下游电梯整机厂商，因此电梯市场的变 化与公司的发展密切相关。从电梯行业的发展历程来看，新梯业务一般是发展 期的收入主要来源，而旧梯更新业务则是进入成熟期以后的收入主要来源。我 国电梯市场起步较晚，目前还是以新梯业务为主。因此，近期影响公司盈利能 力稳定性和连续性的主要因素还是房地产投资规模以及相应的新梯安装。未来 随着电梯保有量的不断上升，旧梯更新业务收入比重将逐步加大，而旧梯更新 业务是一个比较稳定的市场，受房地产市场影响较小，将为公司未来盈利的连 续性和稳定性创造良好的外部环境。

## Freshness Delta
Sources:
- recent_material_announcement | 2026-01-30 | announcement | 2025年度业绩预告
- recent_material_announcement | 2026-01-12 | announcement | 关于为子公司提供担保事项的进展公告
- recent_material_announcement | 2026-02-02 | announcement | 关于对外投资的进展公告
Session:
- session_id: freshness_recent_events
- scope: heading=latest_periodic_like; body=recent_material_announcement; semantic=latest_periodic_like, recent_material_announcement
Selected text:
### Source: recent_material_announcement | 2026-01-30 | announcement | 2025年度业绩预告
[retrieval=body | chunk_kind=text | expansion=same_chunk | heading=三、业绩变动原因说明 | score=0.7409]
报告期内，公司经营业绩出现亏损主要系：一是报告期内，公司部分产品面 临激烈的市场竞争，产品毛利率下降；二是报告期内，子公司中山亿泰纳因临时 停产发生的相关费用增加；三是本期股权激励费用较上期增加。
报告期内，非经常性损益对归属于上市公司股东净利润的影响金额约为 970 万元，主要系本期公司持有的荣旗科技股份确认的公允价值变动收益、减持荣旗 科技股份确认的投资收益及投资重元贰号基金确认的投资收益。

### Source: recent_material_announcement | 2026-01-30 | announcement | 2025年度业绩预告
[retrieval=body | chunk_kind=table_bridge | expansion=table:full_table | heading=一、本期业绩预计情况 | score=0.7216]
[TABLE mode=full_table rows=5/5 cols=3]
bridge_before: □同向上升

□同向下降
heading: 一、本期业绩预计情况
header: ["项 目", "本报告期", "上年同期"]
rows:
["归属于上市公司股东的净 利润", "亏损： 4,900.00 万元- 5,900.00 万元", "盈利： 9,212.33 万元"]
["归属于上市公司股东的扣 除非经常性损益的净利润", "亏损： 5,900.00 万元- 6,900.00 万元", "亏损： 1,289.90 万元"]
["营业收入", "91,000.00 万元- 98,000.00 万元", "95,951.49 万元"]
["扣除后营业收入 [ 注 1]", "89,000.00 万元- 96,000.00 万元", "93,327.79 万元"]
["基本每股收益", "亏损： 0.20 元 / 股- 0.24 元 / 股", "盈利： 0.37 元 / 股"]
bridge_after: 注 1 ：扣除后营业收入指扣除与主营业务无关的业务收入和不具备商业实质的收入后的 营业收入。

### Source: recent_material_announcement | 2026-01-12 | announcement | 关于为子公司提供担保事项的进展公告
[retrieval=body | chunk_kind=text | expansion=same_chunk | heading=二、担保进展情况 | score=0.7157]
近日，公司全资子公司苏州波发特电子科技有限公司（以下简称'波发特' ） 向上海银行股份有限公司苏州分行（以下简称'上海银行'）申请了 5,000.00 万 元的综合授信业务， 公司将在此授信额度内为波发特提供 5,000.00 万元的连带责 任担保，并与上海银行签署《最高额保证合同》（合同编号： ZDB308251659 ）， 保证合同主要内容如下：
债权人：上海银行股份有限公司苏州分行。
2.
保证方式：连带责任保证。
担保的最高主债权限额：主债权余额最高不超过人民币 5,000 万元。
主债权余额 = 已经发生的主债权累计额 -已经偿还的主债权累计额。
若主债权为本外币混用的授信，则主债权最高余额系指等值人民币余额。
保证担保的范围：主债权所达的债权本金、利息、罚息、违约金、赔偿 金以及主合同项下应缴未缴的保证金；与主债权有关的所有银行费用（包括但不 限于开证手续费、信用证修改费、提单背书费、承兑费、托收手续费、风险承担 费）；债权及 / 或担保物权实现费用（包括但不限于催收费用、诉讼费用、保全 费、执行费、律师费、担保物处置费、公告费、拍卖费、过户费、差旅费等）以 及债务人给债权人造成的其他损失。

### Source: recent_material_announcement | 2026-01-12 | announcement | 关于为子公司提供担保事项的进展公告
[retrieval=body | chunk_kind=text | expansion=same_chunk | heading=三、累计对外担保数量及逾期担保数量 | score=0.6939]
截至本公告披露日， 公司及其控股子公司与业务相关方签署的担保协议金额 合计人民币 35,100.00 万元，占公司最近一期经审计归属于母公司所有者权益的
38.80% ，占公司最近一期经审计总资产的 24.01% ；公司及其控股子公司的担保 余额合计人民币 11,556.14 万元，占公司最近一期经审计的归属于母公司所有者 权益的 12.77% ，占公司最近一期经审计总资产的 7.91% ；公司及其控股子公司 未发生违规担保和逾期担保的情形。

### Source: recent_material_announcement | 2026-02-02 | announcement | 关于对外投资的进展公告
[retrieval=body | chunk_kind=text | expansion=neighbor_window | heading=二、交易进展情况 | score=0.6619]
2025 年 12 月 26 日，苏州市世嘉科技股份有限公司（以下简称'公司'或 者'世嘉科技'）召开第五届董事会第十二次会议，审议通过了《关于签署 < 苏 州市世嘉科技股份有限公司关于光彩芯辰（浙江）科技有限公司之投资协议 > 与 < 关于光彩芯辰（浙江）科技有限公司之 B5 轮股东协议 > 的议案》，即：公司拟 通过增资扩股及受让标的公司创始股东部分股权方式取得光彩芯辰（浙江）科技 有限公司（以下简称'标的公司'）共计 20% 股权。本次交易对价为 2.75 亿元， 本次交易完成后本公司持有标的公司共计 20% 的股权（以下简称'本次交易'） ， 具体内容详见公司于 2025 年 12 月 30 日在指定信息披露媒体上披露的《关于对 外投资的公告》（公告编号： 2025-072 ）。
2026 年 1 月 14 日，公司在指定信息披露媒体上披露了《关于对外投资的进 展公告》 （公告编号： 2026-009 ），即公司已向标的公司支付了增资款 1.20 亿元， 同时标的公司已完成相应股权的变更登记。
>>>

Write the Company Wiki in Markdown, targeting 2000-4000 Chinese characters. Use the full target range when the source package contains material recent events, financing, projects, customers, segment data, or broker-only trigger variables. Start with:
# 世嘉科技 (002796) Company Wiki
