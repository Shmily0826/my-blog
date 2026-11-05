import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart';
import 'package:sky_scout/data/models/app_location.dart';
import 'package:sky_scout/features/sky_map/sky_map_page.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SemanticsBinding.instance.ensureSemantics();
  runApp(MaterialApp(
    debugShowCheckedModeBanner: false,
    title: 'Sky Scout interactive demo',
    theme: ThemeData(
      brightness: Brightness.dark,
      fontFamily: 'DemoRoboto',
      colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xffd1bce9), brightness: Brightness.dark),
      scaffoldBackgroundColor: const Color(0xff111520),
    ),
    home: SkyMapPage(
      location: const AppLocation(-36.8485, 174.7633, LocationSource.manual),
      initialTime: DateTime.utc(2026, 11, 5, 9),
    ),
  ));
}
