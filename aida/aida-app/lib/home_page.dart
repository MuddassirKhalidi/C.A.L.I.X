import 'dart:async';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:smooth_page_indicator/smooth_page_indicator.dart';
import 'package:shared_preferences/shared_preferences.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late List<String> _sentences;
  late PageController _pageController;
  final TextEditingController _nameController = TextEditingController();
  String? _storedName;

  @override
  void initState() {
    super.initState();

    _sentences = [
      "Welcome to AIDA!",
      "Your personal voice assistant",
      "Never miss a moment!",
    ];

    _pageController = PageController(
      initialPage: _sentences.length * 1000,
    );

    _loadName();

    Future.delayed(const Duration(seconds: 2), () {
      _startSentenceSwitch();
    });
  }

  void _startSentenceSwitch() {
    Timer.periodic(const Duration(seconds: 5), (timer) {
      int currentPage = _pageController.page!.toInt();
      _pageController.animateToPage(
        currentPage + 1,
        duration: const Duration(seconds: 1),
        curve: Curves.easeInOut,
      );
    });
  }

  Future<void> _loadName() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    setState(() {
      _storedName = prefs.getString('name') ?? '';

      // Capitalize the first letter of the stored name
      if (_storedName!.isNotEmpty) {
        _storedName = _storedName![0].toUpperCase() + _storedName!.substring(1);
      }

      _nameController.text = _storedName!;

      if (_storedName!.isNotEmpty) {
        _sentences.insert(1, "Welcome, $_storedName!");
      }
    });
  }

  Future<void> _saveName() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setString('name', _nameController.text);
    setState(() {
      _storedName = _nameController.text;

      if (_storedName!.isNotEmpty) {
        if (_sentences.contains("Welcome, $_storedName!")) {
          int index = _sentences.indexOf("Welcome, $_storedName!");
          _sentences[index] = "Welcome, $_storedName!";
        } else {
          _sentences.insert(1, "Welcome, $_storedName!");
        }
      }
    });
  }

  @override
  void dispose() {
    _pageController.dispose();
    _nameController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        // Background Image
        Container(
          decoration: const BoxDecoration(
            image: DecorationImage(
                image: AssetImage('assets/IMG_5469.JPG'),
                fit: BoxFit.cover,
                alignment: Alignment.center),
          ),
        ),
        // Foreground content
        Scaffold(
          backgroundColor: Colors.transparent, // Make the Scaffold transparent
          body: Column(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(
                    horizontal: 16.0, vertical: 20.0),
                child: Column(
                  children: [
                    SizedBox(
                      height: 65,
                    ),
                    TextField(
                      controller: _nameController,
                      decoration: InputDecoration(
                        labelText: 'Enter your name',
                        labelStyle: GoogleFonts.robotoMono(
                          textStyle: const TextStyle(
                            color: Colors.white,
                            fontSize: 25,
                          ),
                        ),
                        filled: true,
                        fillColor: Colors.white24,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(8.0),
                          borderSide: BorderSide.none,
                        ),
                      ),
                      style: const TextStyle(
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(height: 10),
                    ElevatedButton(
                      onPressed: _saveName,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Color.fromARGB(159, 51, 2, 82),
                      ),
                      child: Text(
                        'Save Name',
                        style: GoogleFonts.robotoMono(
                          textStyle: const TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 15,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              Expanded(
                child: Stack(
                  children: [
                    PageView.builder(
                      controller: _pageController,
                      itemCount: null,
                      itemBuilder: (context, index) {
                        int sentenceIndex = index % _sentences.length;
                        return Center(
                          child: Text(
                            _sentences[sentenceIndex],
                            style: GoogleFonts.robotoMono(
                              textStyle: const TextStyle(
                                fontSize: 27,
                                color: Color(0xFFCBC5D0),
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            textAlign: TextAlign.center,
                          ),
                        );
                      },
                    ),
                    Align(
                      alignment: Alignment.bottomCenter,
                      child: Padding(
                        padding: const EdgeInsets.only(bottom: 20.0),
                        child: SmoothPageIndicator(
                          controller: _pageController,
                          count: _sentences.length,
                          effect: const WormEffect(
                            activeDotColor: Colors.white,
                            dotColor: Colors.grey,
                            dotHeight: 8.0,
                            dotWidth: 8.0,
                            spacing: 16.0,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 40.0),
            ],
          ),
        ),
      ],
    );
  }
}
