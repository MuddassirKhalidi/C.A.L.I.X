import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(Memoro());
}

class Memoro extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Memory Assistant',
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: Colors.black,
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  List<dynamic> _devices = [];
  bool _isRecording = false;
  final TextEditingController _questionController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _fetchDevices();
  }

  Future<void> _fetchDevices() async {
    final response = await http.get(Uri.parse('http://localhost:5000/devices'));

    if (response.statusCode == 200) {
      setState(() {
        _devices = jsonDecode(response.body);
      });
    } else {
      // Handle error
      print('Failed to load devices');
    }
  }

  Future<void> _recordAudio() async {
    // Placeholder for recording logic
    setState(() {
      _isRecording = !_isRecording;
    });
  }

  Future<void> _askQuestion() async {
    // Placeholder for question handling logic
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: _recordAudio,
              style: ElevatedButton.styleFrom(
                primary: Colors.deepPurple,
                onPrimary: Colors.white,
                padding: EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                textStyle: TextStyle(fontSize: 18),
              ),
              child: Text(
                _isRecording ? 'Stop Recording' : 'Start Recording',
              ),
            ),
            SizedBox(height: 20),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0),
              child: TextField(
                controller: _questionController,
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: 'Ask me a question',
                  fillColor: Colors.white,
                  filled: true,
                ),
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _askQuestion,
              style: ElevatedButton.styleFrom(
                primary: Colors.deepPurple,
                onPrimary: Colors.white,
                padding: EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                textStyle: TextStyle(fontSize: 18),
              ),
              child: Text('Ask Me'),
            ),
            SizedBox(height: 20),
            Expanded(
              child: ListView.builder(
                itemCount: _devices.length,
                itemBuilder: (context, index) {
                  final device = _devices[index];
                  return ListTile(
                    title: Text(device['name']),
                    onTap: () {
                      // Handle device selection
                      print('Selected device index: ${device['index']}');
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
