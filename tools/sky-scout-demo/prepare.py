"""Adapt a clean, pinned Sky Scout export; never modify the owning checkout."""
from pathlib import Path
import shutil
import sys

root = Path(sys.argv[1]).resolve()
flutter = Path(sys.argv[2]).resolve()
own = Path(__file__).resolve().parent
page = root / 'lib/features/sky_map/sky_map_page.dart'
text = page.read_text(encoding='utf-8')

def replace(old, new):
    global text
    assert text.count(old) == 1, f'Upstream patch anchor changed: {old[:75]}'
    text = text.replace(old, new)

replace("import 'dart:async';", "import 'dart:async';\nimport 'portfolio_controls.dart';\nconst _portfolioDemo = true;")
# Dart imports must precede declarations.
text = text.replace("const _portfolioDemo = true;\n", "")
replace("class SkyMapPage extends StatefulWidget {", "const _portfolioDemo = true;\n\nclass SkyMapPage extends StatefulWidget {")
replace("    _compass.start();", "    if (!_portfolioDemo) _compass.start();\n    _resetPortfolioView();")
replace("    _startClock();\n    _selectedStar", "    if (!_portfolioDemo) _startClock();\n    _selectedStar")
replace("    if (_didApplyDesktopWebFraming || !kIsWeb) return;", "    if (_portfolioDemo || _didApplyDesktopWebFraming || !kIsWeb) return;")
replace("    setState(() => _zoom = next);", "    setState(() => _zoom = next);\n    _reportPortfolio();")
replace("    _view.value = SkyView.manual(azimuth: _azimuth, pitch: _pitch);\n  }\n\n  void _startGlide", "    _view.value = SkyView.manual(azimuth: _azimuth, pitch: _pitch);\n    _reportPortfolio();\n  }\n\n  void _startGlide")
replace("    _setTime(time);\n  }", "    _setTime(time);\n    _reportPortfolio();\n  }")
replace("      _focusHighlightedStar();", "      _focusHighlightedStar();\n      _reportPortfolio();")
replace("        _starsError = 'Unable to load the local star catalog.';\n      });", "        _starsError = 'Unable to load the local star catalog.';\n      });\n      _reportPortfolio();")
replace("  void _openSelectedDetail() {", """  void _openSelectedDetail() {
    if (_portfolioDemo) {
      final target = _selectedTargetCoordinates();
      if (target != null) {
        showDialog<void>(context: context, builder: (context) => AlertDialog(
          title: Text(target.$1),
          content: Text('Azimuth ${target.$2.round()}° · Altitude ${target.$3.round()}°'),
          actions: [TextButton(onPressed: () => Navigator.pop(context), child: const Text('Close'))],
        ));
      }
      return;
    }""")
replace("    final toolbar = SkyMapToolbar(", """    final toolbar = _portfolioDemo ? PortfolioControls(
      time: _observationTime, zoom: _zoom,
      onTime: _setManualTime, onZoom: _setZoom, onReset: _resetPortfolioView,
    ) : SkyMapToolbar(""")
replace("                  if (desktopWeb) _buildWebControls(),", "                  if (!_portfolioDemo && desktopWeb) _buildWebControls(),")
replace("      bottomNavigationBar: desktopWeb", "      bottomNavigationBar: !_portfolioDemo && desktopWeb")
marker = "  @override\n  Widget build(BuildContext context) {"
replace(marker, """  void _reportPortfolio() {
    if (!_portfolioDemo) return;
    reportPortfolioState(ready: !_starsLoading && _starsError == null,
      error: _starsError, azimuth: _azimuth, pitch: _pitch, zoom: _zoom, time: _observationTime);
  }

  void _resetPortfolioView() {
    _inertia.stop();
    _azimuth = 60; _pitch = 35; _zoom = 1;
    _view.value = SkyView.manual(azimuth: _azimuth, pitch: _pitch);
    _setManualTime(portfolioInitial);
  }

""" + marker)
page.write_text(text, encoding='utf-8')
shutil.copyfile(own / 'portfolio_controls.dart', page.parent / 'portfolio_controls.dart')
shutil.copyfile(own / 'main.dart', root / 'lib/portfolio_demo.dart')
# Keep only public star data and self-hosted fonts. No .env or map keys.
pubspec = root / 'pubspec.yaml'
spec = pubspec.read_text(encoding='utf-8')
start = spec.index('\nflutter:\n')
end = spec.index('\nflutter_launcher_icons:', start)
spec = spec[:start] + """
flutter:
  uses-material-design: true
  assets:
    - assets/data/stars.json
    - assets/data/constellation_western.json
  fonts:
    - family: DemoRoboto
      fonts:
        - asset: assets/fonts/roboto-regular.ttf

""" + spec[end:]
pubspec.write_text(spec, encoding='utf-8')
fonts = root / 'assets/fonts'
fonts.mkdir(parents=True, exist_ok=True)
shutil.copyfile(flutter / 'bin/cache/artifacts/material_fonts/roboto-regular.ttf', fonts / 'roboto-regular.ttf')
(root / 'web/index.html').write_text("""<!doctype html>
<html lang="en"><head><base href="$FLUTTER_BASE_HREF"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Sky Scout interactive demo</title>
<style>html,body{margin:0;width:100%;height:100%;background:#111520;color:#f3f0f8;font:16px sans-serif}#loading{padding:24px}</style>
</head><body><p id="loading">Loading the night sky…</p><script src="flutter_bootstrap.js" async></script></body></html>""", encoding='utf-8')
(root / 'web/flutter_bootstrap.js').write_text("""{{flutter_js}}
{{flutter_build_config}}
_flutter.loader.load({config: {canvasKitBaseUrl: '/demos/sky-scout/canvaskit/', canvasKitVariant: 'full'}});
""", encoding='utf-8')
print('Prepared pinned Sky Scout demo without credentials or original checkout changes.')
