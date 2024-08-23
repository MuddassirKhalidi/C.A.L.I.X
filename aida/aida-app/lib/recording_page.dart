import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'recording_button.dart';

class RecordingPage extends StatefulWidget {
  final Function(bool) onRecordingStateChanged;

  const RecordingPage({super.key, required this.onRecordingStateChanged});

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
      decoration: const BoxDecoration(
        image: DecorationImage(
          image: AssetImage('assets/IMG_5482.PNG'),
          fit: BoxFit.cover,
        ),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Padding(
            padding: const EdgeInsets.only(
                top: 80.0), // Adjust the padding as needed
            child: Text(
              'Recording',
              style: GoogleFonts.robotoMono(
                textStyle: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Color.fromARGB(255, 219, 197, 255),
                ),
              ),
            ),
          ),
          Center(
            child: RecordingButton(
              isRecording: _isRecording,
              onTap: _toggleRecording,
            ),
          ),
          const SizedBox(height: 40), // Extra spacing at the bottom if needed
        ],
      ),
    );
  }
}
