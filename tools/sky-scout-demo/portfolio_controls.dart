import 'dart:js_interop';
import 'package:flutter/material.dart';

@JS('window.parent.postMessage')
external void _postMessage(JSAny message, JSString origin);
@JS('window.location.origin')
external JSString get _origin;

final portfolioStart = DateTime.utc(2026, 11, 5, 7);
final portfolioInitial = DateTime.utc(2026, 11, 5, 9);

void reportPortfolioState({required bool ready, String? error, required double azimuth, required double pitch, required double zoom, required DateTime time}) {
  _postMessage({
    'type': 'sky-scout-demo-state',
    'ready': ready,
    'error': error,
    'azimuth': azimuth,
    'pitch': pitch,
    'zoom': zoom,
    'minute': time.difference(portfolioStart).inMinutes,
  }.jsify()!, _origin);
}

class PortfolioControls extends StatelessWidget {
  const PortfolioControls({super.key, required this.time, required this.zoom, required this.onTime, required this.onZoom, required this.onReset});
  final DateTime time;
  final double zoom;
  final ValueChanged<DateTime> onTime;
  final ValueChanged<double> onZoom;
  final VoidCallback onReset;

  @override
  Widget build(BuildContext context) {
    final local = time.add(const Duration(hours: 13));
    final label = '${local.hour.toString().padLeft(2, '0')}:${local.minute.toString().padLeft(2, '0')}';
    return Material(
      color: const Color(0xff191e2b),
      child: SafeArea(top: false, child: Padding(
        padding: const EdgeInsets.fromLTRB(12, 8, 12, 8),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Row(children: [
            Expanded(child: Text('Auckland · Nov ${local.day}\n$label NZDT', style: const TextStyle(fontSize: 13))),
            IconButton(tooltip: 'Zoom out', onPressed: zoom > 1 ? () => onZoom(zoom / 1.25) : null, icon: const Icon(Icons.remove)),
            Text('${zoom.toStringAsFixed(1)}×', style: const TextStyle(fontSize: 12)),
            IconButton(tooltip: 'Zoom in', onPressed: zoom < 4 ? () => onZoom(zoom * 1.25) : null, icon: const Icon(Icons.add)),
            IconButton(tooltip: 'Reset sky', onPressed: onReset, icon: const Icon(Icons.restart_alt)),
          ]),
          Semantics(label: 'Observation time', child: Slider(
            value: time.difference(portfolioStart).inMinutes.clamp(0, 240).toDouble(),
            min: 0, max: 240, divisions: 48,
            label: '$label NZDT',
            semanticFormatterCallback: (_) => '$label NZDT',
            onChanged: (value) => onTime(portfolioStart.add(Duration(minutes: value.round()))),
          )),
          const Text('Drag to look around · Pinch or use + / − to zoom', style: TextStyle(fontSize: 11, color: Color(0xffb5b7ca))),
        ]),
      )),
    );
  }
}
