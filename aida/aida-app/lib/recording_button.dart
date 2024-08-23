import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:simple_ripple_animation/simple_ripple_animation.dart';

class RecordingButton extends StatelessWidget {
  final bool isRecording;
  final VoidCallback onTap;

  const RecordingButton({super.key, required this.isRecording, required this.onTap});

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
    return RippleAnimation(
      repeat: true,
      color: isRecording ? Color.fromARGB(255, 138, 19, 162): Color(0xFFBB52DB),
      minRadius: 70,
      ripplesCount: 6,
      child: ElevatedButton(
        onPressed: () async {
          onTap();
          if (isRecording) {
            await _stopListening();
          } else {
            await _listen();
          }
        },
        style: ElevatedButton.styleFrom(
          shape: const CircleBorder(),
          padding: const EdgeInsets.all(20),
          backgroundColor:
              isRecording ? Color.fromARGB(255, 138, 19, 162): Color(0xFFBB52DB),
        ),
        child: Icon(
          isRecording ? Icons.stop : Icons.mic,
          color: Colors.white,
          size: 70,
        ),
      ),
    );
  }
}
