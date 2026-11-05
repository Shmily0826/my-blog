# Sky Scout portfolio demo

This is a focused adaptation of the team's existing Flutter sky map, not a newly written JavaScript imitation.

- Upstream: UOA-CS734-S2-2026/project-implementation-one-to-be-found
- Pinned source: 4fdf1ac943992b8fd5934145b35d734212906123 (main)
- The owner checkout is never changed. A clean Git archive is adapted in a temporary directory.
- The original projection, astronomy calculations, catalog, stars, constellation lines, terrain, gestures and object labels are reused.
- The demo entry skips Welcome, location selection, device sensors, settings, search and network-backed details.
- The preset is Auckland at 22:00 NZDT on 5 November 2026. The time slider spans 20:00–00:00; reset restores the preset.
- The demo runs only when requested by a visitor. Stop removes the iframe and releases its runtime.
- Rendering, fonts, and catalog assets are self-hosted. No map keys, .env files, source maps, provider calls, or service worker are published.
- Parent messages are accepted only from the active iframe at the same origin. They convey readiness/errors and view state; the host DOM records view state for interaction verification.
- Static assets are checked in so Vercel needs only the existing Astro build, not Flutter.

## Rebuild

Use the existing Flutter SDK and a local repository containing the pinned commit:

```powershell
./tools/sky-scout-demo/build.ps1 -SourceRepository <Sky-Scout-checkout> -FlutterRoot <Flutter-SDK>
npm run build
npm run check:rss
```

The SDK's package cache must already contain the locked dependencies. Packaging includes only the JS build, full CanvasKit runtime, public star data and fonts. The exported source and intermediate build remain in a uniquely named temporary directory for inspection.

## Verification

Check that the project page loads no demo assets before Start. After Start, confirm ready, a rendered star field, drag changing azimuth/pitch, zoom buttons and wheel/pinch, time changes moving the sky, and Reset restoring the preset. Test Stop and restart, the standalone route, mobile layout, keyboard time controls and no GPS/camera/provider requests. Build/RSS/draft isolation checks still apply to the whole site.

Credit the team project and original data sources; public attribution is in public/demos/sky-scout/ATTRIBUTION.txt. The source repository remains private; no claim of sole authorship or current live weather is made.
