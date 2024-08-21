import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class AskingButton extends StatelessWidget {
  final bool isAsking;
  final VoidCallback onTap;

  const AskingButton({super.key, required this.isAsking, required this.onTap});
  Future<void> _listen() async {
    final response = await http.get(Uri.parse('http://127.0.0.1:5000/listen'));
    if (response.statusCode == 200) {
      print('Recording started');
    } else {
      print('Error starting recording');
    }
  }

  Future<void> _generateResponse() async {
    final response = await http.get(Uri.parse('http://127.0.0.1:5000/respond'));
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
        if (isAsking) {
          await _generateResponse();
        } else {
          await _listen();
        }
      },
      style: ElevatedButton.styleFrom(
        shape: const CircleBorder(),
        padding: const EdgeInsets.all(20),
        backgroundColor:
            isAsking ? Colors.red : const Color.fromARGB(255, 42, 181, 49),
      ),
      child: Icon(
        isAsking ? Icons.stop : Icons.mic,
        color: Colors.white,
        size: 70,
      ),
    );
  }
}
