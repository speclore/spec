---
guid: 11111111-1111-4111-8111-111111111111
type: folder
author: SpecLore
created: 2026-09-06T10:00:00Z
title: Core example
usage: project
kind: composite
speclore: 0.1.0-core
relation-types:
  - name: depends-on
    inverse: required-by
    cardinality: N:N
    on-delete: restrict
---

A minimal project with two related documents and a derived reference store.
