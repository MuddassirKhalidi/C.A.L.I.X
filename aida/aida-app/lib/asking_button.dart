import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class AskingButton extends StatefulWidget {
  final bool isAsking;
  final VoidCallback onTap;

  const AskingButton({super.key, required this.isAsking, required this.onTap});

  @override
  _AskingButtonState createState() => _AskingButtonState();
}

class _AskingButtonState extends State<AskingButton> {
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
      print('Response generated');
    } else {
      print('Error generating response');
    }
  }

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: () async {
        widget.onTap();
        if (widget.isAsking) {
          await _generateResponse();
        } else {
          await _listen();
        }
      },
      style: ElevatedButton.styleFrom(
        shape: const CircleBorder(),
        padding: const EdgeInsets.all(20),
        backgroundColor: widget.isAsking
            ? const Color.fromARGB(255, 162, 19, 33)
            : const Color(0xFFBB52DB),
      ),
      child: Icon(
        widget.isAsking ? Icons.stop : Icons.mic,
        color: Colors.white,
        size: 70,
      ),
    );
  }
}
