import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Voice Assistant',
      theme: ThemeData(
        primarySwatch: Colors.blue,
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
  final _textController = TextEditingController();
  String _response = '';

  @override
  void initState() {
    super.initState();
    // Example: Initialize something here, such as fetching initial data
    print("Widget initialized!");
  }

  Future<void> _listen() async {
    try {
      final response = await http.get(
        Uri.parse('http://localhost:5000/listen'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        setState(() {
          _response = response.body;
        });
      } else {
        setState(() {
          _response = 'Error: ${response.statusCode}, ${response.body}';
        });
      }
    } catch (e) {
      setState(() {
        _response = 'An error occurred: $e';
      });
      print('An error occurred: $e');
    }
  }

  Future<void> _stopListening() async {
    final response = await http.post(
      Uri.parse('http://localhost:5000/stop_listening'),
      headers: {
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      setState(() {
        _response = 'Stopped listening';
      });
    } else {
      setState(() {
        _response = 'Error: ${response.statusCode}';
      });
    }
  }

  Future<void> _generateResponse() async {
    final response = await http.post(
      Uri.parse('http://localhost:5000/generate_response'),
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({'query': _textController.text}),
    );

    if (response.statusCode == 200) {
      setState(() {
        _response = response.body;
      });
    } else {
      setState(() {
        _response = 'Error: ${response.statusCode}';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Voice Assistant'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _listen,
              child: Text('Listen'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _stopListening,
              child: Text('Stop Listening'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _generateResponse,
              child: Text('Generate Response'),
            ),
            SizedBox(height: 20),
            Text(_response),
          ],
        ),
      ),
    );
  }
}
