"""Copy only the self-contained runtime; exclude credentials, symbols and unused engines."""
from pathlib import Path
import json, shutil, sys
source = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2]).resolve()
flutter = Path(sys.argv[3]).resolve()
expected = Path(__file__).resolve().parents[2] / 'public/demos/sky-scout'
assert output == expected.resolve(), 'Unexpected publish directory'
output.mkdir(parents=True, exist_ok=True)
selected = []
for path in source.rglob('*'):
    if not path.is_file(): continue
    rel = path.relative_to(source)
    keep = (rel.as_posix() in ['index.html', 'flutter_bootstrap.js', 'main.dart.js', 'version.json']
            or rel.parts[0] == 'assets'
            or rel.as_posix() in ['canvaskit/canvaskit.js', 'canvaskit/canvaskit.wasm'])
    if not keep: continue
    assert path.name != '.env' and path.suffix != '.map'
    target = output / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, target)
    selected.append(rel.as_posix())
bootstrap = output / 'flutter_bootstrap.js'
loader = "_flutter.loader.load({config: {canvasKitBaseUrl: '/demos/sky-scout/canvaskit/', canvasKitVariant: 'full'}});"
bootstrap_text = bootstrap.read_text(encoding='utf-8')
assert bootstrap_text.count(loader) == 1
bootstrap.write_text(bootstrap_text.replace(loader, """const demoConfig = {canvasKitBaseUrl: '/demos/sky-scout/canvaskit/', canvasKitVariant: 'full'};
_flutter.loader.load({config: demoConfig, onEntrypointLoaded: async (initializer) => {
  const runner = await initializer.initializeEngine(demoConfig);
  await runner.runApp();
  document.getElementById('loading')?.remove();
}});"""), encoding='utf-8')
shutil.copyfile(flutter / 'bin/cache/artifacts/material_fonts/roboto_license.txt', output / 'ROBOTO-LICENSE.txt')
(output / 'build-info.json').write_text(json.dumps({
    'sourceCommit': '4fdf1ac943992b8fd5934145b35d734212906123',
    'adaptation': 'tools/sky-scout-demo',
    'preset': 'Auckland, 2026-11-05 22:00 NZDT',
    'files': selected,
}, indent=2) + '\n', encoding='utf-8')
assert not any(p.name == '.env' for p in output.rglob('*'))
assert (output / 'canvaskit/canvaskit.wasm').exists()
print(f'Packaged {len(selected)} runtime files, {sum((output / p).stat().st_size for p in selected):,} bytes.')
