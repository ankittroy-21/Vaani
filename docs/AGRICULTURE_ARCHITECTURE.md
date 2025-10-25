# Agriculture Module Architecture

## System Architecture Overview

```
┌────────────────────────────────────────────────────────────────┐
│                        User Input                              │
│              "आलू का भाव क्या है?"                             │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│              Main Command Processor                            │
│         agri_command_processor.py                              │
│  ┌─────────────────────────────────────────────────┐          │
│  │  1. Check Context (awaiting_agri_response?)    │          │
│  │  2. Keyword-Based Intent Detection              │          │
│  │     - Price keywords?                            │          │
│  │     - Scheme keywords?                           │          │
│  │     - Advisory keywords?                         │          │
│  │  3. Route to appropriate service                │          │
│  └─────────────────────────────────────────────────┘          │
└───────┬──────────────┬──────────────┬─────────────────────────┘
        │              │              │
        ▼              ▼              ▼
┌───────────┐  ┌───────────┐  ┌──────────────┐
│  Price    │  │  Scheme   │  │   Advisory   │
│  Service  │  │  Service  │  │   Service    │
└───────────┘  └───────────┘  └──────────────┘
```

---

## Service Architecture Details

### 1. Price Service Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Price Service                            │
│                agri_price_service.py                        │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
      ┌─────────────┐
      │ Extract     │
      │ Entities    │
      │ (crop,      │
      │  market,    │
      │  state)     │
      └──────┬──────┘
             │
             ▼
      ┌──────────────────┐
      │ Check Cache      │
      │ (6-hour TTL)     │
      └─────┬────────────┘
            │
      ┌─────┴─────┐
      │ Hit? Miss?│
      └─────┬─────┘
            │
    ┌───────┴────────┐
    │                │
    ▼                ▼
┌────────┐      ┌─────────────┐
│ Return │      │  API Call   │
│ Cached │      │ Agmarknet   │
│  Data  │      │ (10s timeout│
└────────┘      └──────┬──────┘
                       │
                 ┌─────┴──────┐
                 │ Success?   │
                 │  Failure?  │
                 └──────┬─────┘
                        │
               ┌────────┴────────┐
               │                 │
               ▼                 ▼
        ┌──────────┐      ┌──────────────┐
        │ Cache &  │      │ Try Offline  │
        │ Return   │      │ Cache        │
        └──────────┘      └──────┬───────┘
                                 │
                          ┌──────┴───────┐
                          │ Available?   │
                          └──────┬───────┘
                                 │
                        ┌────────┴────────┐
                        │                 │
                        ▼                 ▼
                  ┌──────────┐    ┌────────────┐
                  │ Return   │    │ Hardcoded  │
                  │ Offline  │    │ Fallback   │
                  └──────────┘    └────────────┘
```

### 2. Advisory Service Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Advisory Service                          │
│              agri_advisory_service.py                       │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
      ┌──────────────┐
      │ Extract Crop │
      │ from Command │
      └──────┬───────┘
             │
             ▼
      ┌──────────────────┐
      │ Check Crop Cache │
      │ (In-memory dict) │
      └─────┬────────────┘
            │
      ┌─────┴─────┐
      │ Cached?   │
      └─────┬─────┘
            │
    ┌───────┴────────┐
    │                │
    ▼                ▼
┌────────┐    ┌────────────────┐
│ Return │    │ Load from File │
│ Cache  │    │ data/crop_data/│
└────────┘    └────────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ Parse Stage  │
                │ (बुवाई, etc) │
                └──────┬───────┘
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
       ┌───────────┐    ┌───────────────┐
       │ Full Info │    │ Specific Stage│
       │ Request?  │    │ Information   │
       └───────────┘    └───────────────┘
```

### 3. Scheme Service Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Scheme Service                           │
│               agri_scheme_service.py                        │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
      ┌────────────────┐
      │ Parse Query    │
      │ Type           │
      └────────┬───────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
┌─────────┐         ┌──────────┐
│ Scheme  │         │ Subsidy  │
│ Name    │         │ Query    │
└────┬────┘         └─────┬────┘
     │                    │
     ▼                    ▼
┌──────────────┐   ┌─────────────────┐
│ Match        │   │ Extract Crop    │
│ Keywords     │   │ from Command    │
└──────┬───────┘   └────────┬────────┘
       │                    │
       ▼                    ▼
┌──────────────┐   ┌─────────────────┐
│ Load Scheme  │   │ Load Subsidy    │
│ Data         │   │ Data            │
└──────┬───────┘   └────────┬────────┘
       │                    │
       └──────────┬─────────┘
                  │
                  ▼
           ┌──────────────┐
           │ Speak Details│
           │ - Name       │
           │ - Description│
           │ - Eligibility│
           │ - Benefits   │
           │ - Process    │
           └──────────────┘
```

---

## Data Flow Diagram

```
┌─────────────┐
│   User      │
│   Query     │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Command Processor│  ◄─────── Context Manager
└──────┬───────────┘           (State/Topic/Data)
       │
       ▼
┌──────────────────┐
│  Intent Detection│
│  (Keywords)      │
└──────┬───────────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌─────┐ ┌─────┐ ┌─────┐
│Price│ │Scheme│ │Advis│
└──┬──┘ └──┬──┘ └──┬──┘
   │       │       │
   └───────┼───────┘
           │
           ▼
    ┌──────────────┐
    │  Data Layer  │
    ├──────────────┤
    │ • Cache      │
    │ • API        │
    │ • Files      │
    │ • Fallback   │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  Response    │
    │  Formatter   │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  Voice/Text  │
    │  Output      │
    └──────────────┘
```

---

## Caching Strategy

```
┌─────────────────────────────────────────────────────┐
│              Cache Architecture                     │
└─────────────────────────────────────────────────────┘

Level 1: In-Memory Cache (Price Service)
┌───────────────────────────────────────┐
│  Key: "आलू_लखनऊ_उत्तर_प्रदेश"        │
│  Value: (price_data, timestamp)      │
│  TTL: 6 hours                        │
└───────────────────────────────────────┘

Level 2: In-Memory Cache (Advisory Service)
┌───────────────────────────────────────┐
│  Key: "गेहूं"                         │
│  Value: crop_json_data               │
│  TTL: Until restart                  │
└───────────────────────────────────────┘

Level 3: Offline Cache (Files)
┌───────────────────────────────────────┐
│  Location: data/offline_cache/       │
│  Format: JSON files                  │
│  Update: Manual                      │
└───────────────────────────────────────┘

Level 4: Hardcoded Fallback
┌───────────────────────────────────────┐
│  Location: Code constants            │
│  Purpose: Last resort                │
│  Coverage: Major commodities         │
└───────────────────────────────────────┘
```

---

## Error Handling Flow

```
┌────────────┐
│  Request   │
└─────┬──────┘
      │
      ▼
┌──────────────┐
│ Try Primary  │
│ Method       │
└─────┬────────┘
      │
  ┌───┴───┐
  │Success│Fail
  │       │
  ▼       ▼
┌────┐  ┌──────────────┐
│Done│  │ Log Error    │
└────┘  │ Try Fallback │
        └─────┬────────┘
              │
          ┌───┴───┐
          │Success│Fail
          │       │
          ▼       ▼
        ┌────┐  ┌──────────────┐
        │Done│  │ Log Error    │
        └────┘  │ User Message │
                │ Return Error │
                └──────────────┘
```

---

## Component Interaction Matrix

```
┌──────────────┬──────────┬──────────┬──────────┬──────────┐
│ Component    │ Processor│  Price   │  Scheme  │ Advisory │
├──────────────┼──────────┼──────────┼──────────┼──────────┤
│ Processor    │    -     │  Routes  │  Routes  │  Routes  │
├──────────────┼──────────┼──────────┼──────────┼──────────┤
│ Price        │  Returns │    -     │    -     │    -     │
├──────────────┼──────────┼──────────┼──────────┼──────────┤
│ Scheme       │  Returns │    -     │    -     │    -     │
├──────────────┼──────────┼──────────┼──────────┼──────────┤
│ Advisory     │  Returns │    -     │    -     │    -     │
├──────────────┼──────────┼──────────┼──────────┼──────────┤
│ Context      │   Uses   │    -     │   Uses   │   Uses   │
├──────────────┼──────────┼──────────┼──────────┼──────────┤
│ Config       │   Reads  │  Reads   │  Reads   │  Reads   │
├──────────────┼──────────┼──────────┼──────────┼──────────┤
│ Logger       │   Logs   │  Logs    │  Logs    │  Logs    │
└──────────────┴──────────┴──────────┴──────────┴──────────┘
```

---

## Module Dependencies

```
agri_command_processor
    ├── agri_price_service
    │   ├── requests
    │   ├── logging
    │   ├── datetime
    │   └── config
    ├── agri_scheme_service
    │   ├── json
    │   ├── os
    │   ├── logging
    │   └── config
    └── agri_advisory_service
        ├── json
        ├── os
        ├── logging
        └── config
```

---

## State Machine (Context Management)

```
┌─────────────┐
│   Initial   │
│   State     │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ User Query       │
└──────┬───────────┘
       │
       ▼
┌──────────────────────┐
│ awaiting_agri_response│◄──┐
│ (Context Set)         │   │
└──────┬────────────────┘   │
       │                    │
       ▼                    │
┌──────────────────┐        │
│ User Responds    │        │
└──────┬───────────┘        │
       │                    │
   ┌───┴───┐               │
   │Match? │               │
   └───┬───┘               │
       │                   │
   ┌───┴───┐              │
   │Yes│No │              │
   │   │   │              │
   ▼   ▼   └──────────────┘
┌────┐ ┌─────────────┐
│Done│ │ Ask Again   │
└────┘ └─────────────┘
```

---

**Architecture Diagram v2.0** | Last Updated: October 25, 2025
