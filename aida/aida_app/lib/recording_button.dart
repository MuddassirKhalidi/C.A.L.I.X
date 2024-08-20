import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class RecordingButton extends StatelessWidget {
  final bool isRecording;
  final VoidCallback onTap;

  const RecordingButton({required this.isRecording, required this.onTap});

  Future<void> _listen() async {
    final response = await http.get(Uri.parse('http://127.0.0.1:5000/listen'));
    if (response.statusCode == 200) {
      print('Recording started');
    } else {
      print('Error starting recording');
    }
  }

  Future<void> _stopListening() async {
    final response = await http.get(Uri.parse('http://127.0.0.1:5000/stop'));
    if (response.statusCode == 200) {
      print('Recording stopped');
    } else {
      print('Error stopping recording');
    }
  }

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: () async {
        onTap();
        if (isRecording) {
          await _stopListening();
        } else {
          await _listen();
        }
      },
      style: ElevatedButton.styleFrom(
        shape: CircleBorder(),
        padding: EdgeInsets.all(20),
        backgroundColor:
            isRecording ? Colors.red : const Color.fromARGB(255, 42, 181, 49),
      ),
      child: Icon(
        isRecording ? Icons.stop : Icons.mic,
        color: Colors.white,
        size: 70,
      ),
    );
  }
}
