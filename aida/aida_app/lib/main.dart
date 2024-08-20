import 'package:flutter/material.dart';
import 'home_page.dart';
import 'recording_page.dart';
import 'asking_page.dart';

void main() {
  runApp(AIDA());
}

class AIDA extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AIDA',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      debugShowCheckedModeBanner: false,
      home: MainPage(),
    );
  }
}

class MainPage extends StatefulWidget {
  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int _selectedIndex = 0;
  bool _isRecording = false;
  bool _isAsking = false;

  List<Widget> _pages = [];

  @override
  void initState() {
    super.initState();
    _pages = [
      HomePage(),
      RecordingPage(
        onRecordingStateChanged: (isRecording) {
          setState(() {
            _isRecording = isRecording;
          });
        },
      ),
      AskingPage(
        onAskingStateChanged: (isAsking) {
          setState(() {
            _isAsking = isAsking;
          });
        },
      ),
    ];
  }

  void _onItemTapped(int index) {
    if (_isRecording || _isAsking) return;
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Center(
          child: Text(
            _selectedIndex == 0
                ? "Welcome to AIDA"
                : _selectedIndex == 1
                    ? "Record Conversation"
                    : "Asking",
            style: TextStyle(
              fontSize: 24,
              color: Color(0xFF6A0DAD),
              fontFamily: 'OpenSans',
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        backgroundColor: Colors.white,
        elevation: 0,
      ),
      body: IndexedStack(
        index: _selectedIndex,
        children: _pages,
      ),
      bottomNavigationBar: BottomNavigationBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.mic),
            label: 'Record',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.question_answer),
            label: 'Ask',
          ),
        ],
        currentIndex: _selectedIndex,
        selectedItemColor: Color(0xFFAB3CFF),
        onTap: _onItemTapped,
        backgroundColor:
            _isRecording || _isAsking ? Colors.grey[300] : Colors.white,
        elevation: _isRecording || _isAsking ? 0 : 8,
      ),
    );
  }
}
