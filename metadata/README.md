# Realsee3D Dataset Statistics

This document provides a detailed statistical analysis of the Realsee3D dataset. The dataset is composed of two primary subsets: real-world scenes captured with 3D scanners and procedurally generated synthetic scenes.

## Semantic Segmentation Class Mappings

The label tables for the per-viewpoint `segment.png` maps live alongside this file as JSON. Each table carries the class names (English/Chinese) and a fixed, deterministic official RGB colour palette (label ID 0 = background → black).

| Subset | File | Classes |
| :--- | :--- | :--- |
| Real-world | [`class_mapping_real.json`](class_mapping_real.json) | 150 (IDs 1–197, flat) |
| Synthetic | [`class_mapping_synthetic.json`](class_mapping_synthetic.json) | 209 (IDs 1–209, three-level taxonomy) |

### JSON schema

Top-level object:

| Field | Type | Description |
| :--- | :--- | :--- |
| `subset` | string | `"real"` or `"synthetic"`. |
| `description` | string | Human-readable summary of the label space. |
| `num_classes` | int | Number of labelled classes (excludes the background id 0). |
| `ignore_id` | int | Reserved background / unlabeled / invalid label. Always `0`. |
| `hierarchical` | bool | `true` for the synthetic subset, `false` for real-world. |
| `label_source` | string | `"model_prediction"` (real-world) or `"rendered_ground_truth"` (synthetic). See note below. |
| `classes` | array | List of class entries (see below), sorted by `id`. |

> **Note:** Real-world `segment.png` maps are **predictions from our own trained model**, not manual annotation, and may contain errors. Synthetic maps are exact labels rendered from the scene definition. Human-verified ground-truth annotations for the real-world subset are planned for a future release.

Each entry in `classes`:

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | int | Pixel value used in `segment.png`. |
| `name` | string | English class name. For the synthetic subset this is the full `level1/level2/level3` path. |
| `name_zh` | string | Chinese class name (mirrors the path for the synthetic subset). |
| `color` | [int, int, int] | Official RGB palette colour, 0–255. |
| `taxonomy` | object | **Synthetic only.** Three-level taxonomy `{ "level1", "level2", "level3" }`; absent levels are `null`. |

Example entry (synthetic):

```json
{
  "id": 91,
  "name": "basic/wall/wall_cloth",
  "name_zh": "硬装/墙面/壁布",
  "color": [85, 126, 242],
  "taxonomy": { "level1": "basic", "level2": "wall", "level3": "wall_cloth" }
}
```

Loading example:

```python
import json
m = json.load(open("metadata/class_mapping_synthetic.json", encoding="utf-8"))
id2name  = {c["id"]: c["name"]  for c in m["classes"]}
id2color = {c["id"]: c["color"] for c in m["classes"]}
# group all classes under a top-level taxonomy level
level1 = {c["taxonomy"]["level1"] for c in m["classes"]}
```

See [`../DATASET_STRUCTURE.md`](../DATASET_STRUCTURE.md) for how `segment.png` is encoded and visualized.

## Real-World Scene Statistics (1,000 Scenes)

The following analysis pertains to the 1,000 professionally captured real-world residential scenes.

### Architectural Composition

| Metric                        | Value  |
| ----------------------------- | ------ |
| Total Scanned Scenes          | 1,000  |
| Total Rooms                   | 9,483  |
| Average Rooms per Scene       | 9.48   |

### Viewpoint Statistics

| Metric                   | Value   |
| :----------------------- | :------ |
| Total Viewpoints         | 24,263  |
| Average Viewpoints per Scene | 24.2  |

### Floor Distribution

| Number of Floors per Scene | Scene Count |
| -------------------------- | ----------- |
| 1                          | 917         |
| 2                          | 64          |
| 3                          | 19          |

### Room Type Distribution

| Room Type | Count | Percentage |
| :--- | :--- | :--- |
| Bedroom | 3,091 | 32.59% |
| Bathroom | 2,049 | 21.61% |
| Balcony | 1,015 | 10.70% |
| Living Room | 992 | 10.46% |
| Kitchen | 908 | 9.57% |
| Corridor | 658 | 6.94% |
| Study Room | 156 | 1.64% |
| Entrance Hall | 114 | 1.20% |
| Dining Room | 95 | 1.00% |
| Cloakroom | 93 | 0.98% |
| Storage Room | 84 | 0.89% |
| Terrace | 56 | 0.59% |
| Washroom | 48 | 0.51% |
| Stairwell | 35 | 0.37% |
| Elevator | 25 | 0.26% |
| Multifunction Room | 16 | 0.17% |
| Foyer | 14 | 0.15% |
| Other | 13 | 0.14% |
| Laundry Room | 8 | 0.08% |
| Shower Room | 5 | 0.05% |
| Nanny's Room | 3 | 0.03% |
| Sunroom | 1 | 0.01% |
| Lounge/Water Bar | 1 | 0.01% |
| Reception Area | 1 | 0.01% |
| Negotiation Room | 1 | 0.01% |
| Drying Area | 1 | 0.01% |
| **Total** | **9,483** | **100.00%** |

### Architectural Element Distribution

This table details the frequency of various architectural elements such as doors and windows.

| Element Type | Count |
| :--- | :--- |
| Single Door | 8,924 |
| Doorway/Opening | 6,756 |
| Standard Window | 4,331 |
| Sliding Door | 3,015 |
| French Window | 2,676 |
| Floor-to-ceiling Single Bay Window | 1,105 |
| Standard Single Bay Window | 550 |
| Double Door | 72 |
| Elevator Door | 52 |
| Standard Bay Window | 25 |
| Floor-to-ceiling Bay Window | 12 |

---

## Procedurally Generated Scene Statistics (9,000 Scenes)

The following analysis pertains to the 9,000 procedurally generated synthetic scenes.

### Architectural Composition

| Metric                        | Value  |
| ----------------------------- | ------ |
| Total Generated Scenes        | 9,000  |
| Total Rooms                   | 86,479 |
| Average Rooms per Scene       | 9.61   |

### Floor Distribution

| Number of Floors per Scene | Scene Count |
| -------------------------- | ----------- |
| 1                          | 9,000       |

### Room Type Distribution

| Room Type (Translated) | Count | Percentage |
| :--- | :--- | :--- |
| Bedroom | 28,601 | 33.07% |
| Bathroom | 16,425 | 18.99% |
| Balcony | 12,432 | 14.38% |
| Living Room | 8,993 | 10.40% |
| Kitchen | 8,727 | 10.09% |
| Corridor | 4,829 | 5.58% |
| Storage Room | 1,765 | 2.04% |
| Dining Room | 1,710 | 1.98% |
| Cloakroom | 965 | 1.12% |
| Study Room | 826 | 0.95% |
| Entrance Hall | 766 | 0.89% |
| Washroom | 167 | 0.19% |
| Other | 143 | 0.17% |
| Foyer | 51 | 0.06% |
| Nanny's Room | 43 | 0.05% |
| Shower Room | 30 | 0.03% |
| Lounge | 3 | 0.00% |
| Open Kitchen | 3 | 0.00% |
| **Total** | **86,479** | **100.00%** |

### Architectural Element Distribution

This table details the frequency of various architectural elements such as doors and windows.

| Element Type (Translated) | Count |
| :--- | :--- |
| Single Door | 106,655 |
| Standard Window | 50,217 |
| Doorway/Opening | 25,591 |
| Sliding Door | 24,050 |
| French Window | 21,759 |
| Folding Door | 7,750 |
| Floor-to-ceiling Single Bay Window | 6,592 |
| Standard Single Bay Window | 3,709 |
| Door-Window Combination | 3,660 |
| Standard Bay Window | 1,514 |
| Floor-to-ceiling Bay Window | 1,120 |
| Double Door | 350 |
| Elevator Door | 9 |

### Model Distribution

| Metric | Value |
| :--- | :--- |
| Total Unique Models in All Scenes | 13,684 |
| Average Models per Scene (including duplicates) | 511.14 |

### Viewpoint Statistics

| Metric                   | Value    |
| :----------------------- | :------- |
| Total Viewpoints         | 274,810  |
| Average Viewpoints per Scene | 30.5   |

