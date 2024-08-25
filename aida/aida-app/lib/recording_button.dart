import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class RecordingButton extends StatefulWidget {
  final bool isRecording;
  final VoidCallback onTap;

  const RecordingButton(
      {super.key, required this.isRecording, required this.onTap});

  @override
  _RecordingButtonState createState() => _RecordingButtonState();
}

class _RecordingButtonState extends State<RecordingButton> {
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
        widget.onTap();
        if (widget.isRecording) {
          await _stopListening();
        } else {
          await _listen();
        }
      },
      style: ElevatedButton.styleFrom(
        shape: const CircleBorder(),
        padding: const EdgeInsets.all(20),
        backgroundColor: widget.isRecording
            ? const Color.fromARGB(255, 162, 19, 33)
            : const Color(0xFFBB52DB),
      ),
      child: Icon(
        widget.isRecording ? Icons.stop : Icons.mic,
        color: Colors.white,
        size: 70,
      ),
    );
  }
}
