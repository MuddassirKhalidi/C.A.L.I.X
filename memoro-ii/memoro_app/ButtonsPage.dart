// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:memoro_app3/AskingButton.dart';
import 'package:memoro_app3/recordingButton.dart';

class ButtonsPage extends StatefulWidget {
  @override
  _ButtonsPageState createState() => _ButtonsPageState();
}

class _ButtonsPageState extends State<ButtonsPage> {
  bool _isRecording = false;
  bool _isAsking = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Center(
          child: Text(
            "AIDA",
            style: TextStyle(
              fontSize: 24,
              color: const Color.fromARGB(255, 97, 1, 114),
              fontFamily: 'OpenSans',
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ),
      backgroundColor: const Color.fromARGB(123, 0, 0, 0),
      body: Column(
        children: <Widget>[
          Expanded(
            child: RecordingButton(
              isRecording: _isRecording,
              onTap: () {
                setState(() {
                  _isRecording = !_isRecording;
                });
              },
            ),
          ),
          Expanded(
            child: AskingButton(
              isAsking: _isAsking,
              onTap: () {
                setState(() {
                  _isAsking = !_isAsking;
                });
              },
            ),
          ),
          SizedBox(
            height: 20.0,
          ),
        ],
      ),
    );
  }
}
