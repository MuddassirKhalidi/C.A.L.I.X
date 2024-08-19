// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:aida_app/IntroductionPage.dart';

void main() {
  runApp(AIDA());
}

class AIDA extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: IntroductionPage(),
    );
  }
}
