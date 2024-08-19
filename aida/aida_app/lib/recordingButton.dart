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
    final response = await http.get(Uri.parse('http://127.0.0.1:5000/stop_listening'));
    if (response.statusCode == 200) {
      print('Recording stopped');
    } else {
      print('Error stopping recording');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: GestureDetector(
        onTap: () {
          onTap(); // Toggle the recording state
          if (isRecording) {
            _stopListening(); // Call the stop listening API
          } else {
            _listen(); // Call the listen API
          }
        },
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 120,
              height: 120,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: isRecording
                    ? Colors.red
                    : const Color.fromARGB(255, 39, 176, 92),
                boxShadow: [
                  BoxShadow(
                    offset: Offset(0, 15),
                    blurRadius: 25,
                    color: const Color.fromARGB(186, 0, 0, 0),
                  ),
                ],
              ),
              child: Icon(
                isRecording ? Icons.stop : Icons.mic,
                size: 60,
                color: Color.fromARGB(255, 203, 197, 208),
              ),
            ),
            SizedBox(width: 16),
            Text(
              isRecording ? 'Stop Recording' : 'Click to Start Recording',
              style: TextStyle(
                fontSize: 18,
                fontFamily: 'OpenSans',
                fontWeight: FontWeight.bold,
                color: Color.fromARGB(255, 203, 197, 208),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
