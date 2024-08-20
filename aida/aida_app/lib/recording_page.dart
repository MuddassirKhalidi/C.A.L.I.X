import 'package:flutter/material.dart';
import 'recording_button.dart';

class RecordingPage extends StatefulWidget {
  final Function(bool) onRecordingStateChanged;

  RecordingPage({required this.onRecordingStateChanged});

  @override
  _RecordingPageState createState() => _RecordingPageState();
}

class _RecordingPageState extends State<RecordingPage> {
  bool _isRecording = false;

  void _toggleRecording() {
    setState(() {
      _isRecording = !_isRecording;
    });
    widget.onRecordingStateChanged(_isRecording);
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            Color(0xFF000000),
            Color(0xFF300063),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
      ),
      child: Center(
        child: RecordingButton(
          isRecording: _isRecording,
          onTap: _toggleRecording,
        ),
      ),
    );
  }
}
