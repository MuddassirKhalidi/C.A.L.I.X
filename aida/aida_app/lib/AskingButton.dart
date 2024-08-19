import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class AskingButton extends StatefulWidget {
  final bool isAsking;
  final VoidCallback onTap;

  const AskingButton({required this.isAsking, required this.onTap});

  @override
  _AskingButtonState createState() => _AskingButtonState();
}

class _AskingButtonState extends State<AskingButton> {
  bool _isAsking = false; // Local state to control the button color
  String _statusMessage = ""; // Status message to display

  Future<void> _listen() async {
    try {
      final response = await http.get(Uri.parse('http://127.0.0.1:5000/listen'));
      if (response.statusCode == 200) {
        print('Recording started');
        setState(() {
          _statusMessage = "Query is being recorded...";
        });
      } else {
        print('Error starting recording: ${response.statusCode}');
        setState(() {
          _statusMessage = "Error starting recording.";
        });
      }
    } catch (e) {
      print('Error starting recording: $e');
      setState(() {
        _statusMessage = "Error starting recording.";
      });
    }
  }

  Future<void> _generateResponse() async {
    setState(() {
      _statusMessage = "Query recorded. Processing...";
    });

    try {
      final response = await http.get(Uri.parse('http://127.0.0.1:5000/generate_response'));
      if (response.statusCode == 200) {
        print('Response generated');
        // Update the local state to turn the button green and indicate completion
        setState(() {
          _isAsking = false;
          _statusMessage = "Query processed. You can ask another question.";
        });
      } else {
        print('Error generating response: ${response.statusCode}');
        setState(() {
          _statusMessage = "Error processing query.";
        });
      }
    } catch (e) {
      print('Error generating response: $e');
      setState(() {
        _statusMessage = "Error processing query.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          GestureDetector(
            onTap: () {
              if (_isAsking) {
                // Call the backend and wait for response
                _generateResponse();
              } else {
                // Start listening
                _listen();
                setState(() {
                  _isAsking = true; // Turn the button red immediately
                });
              }
              widget.onTap(); // Notify the parent widget
            },
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 120,
                  height: 120,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: _isAsking
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
                    _isAsking ? Icons.stop : Icons.mic,
                    size: 60,
                    color: Color.fromARGB(255, 203, 197, 208),
                  ),
                ),
                SizedBox(width: 16),
                Text(
                  _isAsking ? 'Finish Asking' : 'Click to Start Asking',
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
          SizedBox(height: 20),
          Text(
            _statusMessage,
            style: TextStyle(
              fontSize: 16,
              fontFamily: 'OpenSans',
              fontWeight: FontWeight.w500,
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
  }
}
