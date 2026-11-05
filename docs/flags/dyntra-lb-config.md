---
title: dyntra_lb_config
---

# `dyntra_lb_config`

> DyntraLB：PD 分离架构 D 节点的负载均衡配置。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active（v0.30.0 新增） |
| 嵌套位置 | `scheduler_config.dyntra_lb_config` |

## 说明

在 PD（Prefill/Decode）分离部署中，动态将解码请求分发到负载更低的 D 节点，缓解请求倾斜导致的尾延迟。

具体子字段以对应版本的官方文档为准。
