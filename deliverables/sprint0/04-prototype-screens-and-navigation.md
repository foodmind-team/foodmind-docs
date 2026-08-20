# Prototype Screens and User Navigation

## Reused FoodMind screens

These are copies of the original UX assets in the Web and Android repositories. They are not newly generated mockups.

### Web recommendation-first home

![Web recommendation-first home](assets/web-recommendation-home.png)

The desktop layout makes **Eat Out & Delivery** and **Cooking** the primary mode choice, places the recommendation context and generation action in the first viewport, and keeps recent decisions and supporting destinations secondary.

### Responsive Web home

![Responsive Web recommendation home](assets/web-recommendation-home-mobile.png)

The mobile-width Web layout retains the same task order while reducing the content to a single-column decision flow.

### Android recommendation-first home

![Android recommendation-first home](assets/android-recommendation-home.png)

The Android prototype uses native touch targets and labelled bottom navigation while preserving the same core modes and destinations.

### Permission-safe Explore

![Web Explore feed](assets/web-explore-feed.png)

Explore is an image-led discovery surface assembled from authorised group-visible records and curated platform content. It is not a public follower feed and does not imply unrestricted internet search.

## Primary recommendation journey

```mermaid
flowchart TD
    A[Open Home] --> B{Choose mode}
    B -->|Eat Out and Delivery| C[Enter area, budget,<br/>occasion, and constraints]
    B -->|Cooking| D[Enter servings, time,<br/>dietary rules, and pantry context]
    C --> E[Optionally choose a<br/>trusted-group context]
    E --> F[Generate recommendation]
    F --> G[Read the lead result,<br/>reason, and evidence]
    G --> H{Decision}
    H -->|Try another| I[Cycle to the next candidate<br/>in the same result set]
    I --> G
    H -->|Accept| J[Store explicit acceptance]
    H -->|Reject| K[Choose a rejection reason]
    J --> L[Later add rating and<br/>Would Eat Again]
    K --> M[Request a new recommendation<br/>when appropriate]
    D --> N[Generate structured<br/>cooking plan]
    N --> O[Review ingredients,<br/>steps, warnings, and source]
```

## Global navigation

| Destination | User purpose | Key return path |
|---|---|---|
| Home | Generate and review recommendations or cooking plans | Recommendation result returns to context without losing the user's draft. |
| Groups | Manage trusted groups, read the group feed, and share selected results | Group context can be selected during recommendation generation. |
| Explore | Discover accessible group or catalogue items and save Want to Try | A detail view returns to the same Explore state. |
| Saved | Revisit Want to Try, recipes, inventory, and related saved workflows | A saved item can become decision context. |
| Me / Profile | Manage identity and preferences and open personal history | Updated preferences apply to later requests through the Backend. |
| Chat | Search, compare, and summarise authorised FoodMind content | Source cards lead back to the referenced platform item. |
| Dashboard | Review personal metrics and weekly recap | Metrics lead back to the underlying records where supported. |

## Prototype scope and provenance

The source assets are:

- workspace-root `foodmind-web/docs/ux/today-dashboard-web.png`;
- workspace-root `foodmind-web/docs/ux/today-dashboard-mobile-web.png`;
- workspace-root `foodmind-web/docs/ux/explore-feed-web.png`;
- workspace-root `foodmind-android/docs/ux/today-dashboard-android.png`.

The navigation explanation reuses the UX README files and slides 7–9 of the feature deck. Images under `Xiaohongshu_UI/` were reference-product research and are intentionally not presented here as FoodMind prototypes.
