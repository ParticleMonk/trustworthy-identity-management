import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:path_provider/path_provider.dart';
import 'package:http/http.dart' as http;
import 'dart:async';
import 'dart:io';

void main() => runApp(MaterialApp(home: CameraApp()));

class CameraApp extends StatefulWidget {
  @override
  _CameraAppState createState() => _CameraAppState();
}

class _CameraAppState extends State<CameraApp> {
  late CameraController controller;
  late List<CameraDescription> cameras;

  @override
  void initState() {
    super.initState();
    availableCameras().then((availableCameras) {
      cameras = availableCameras;
      if (cameras.isNotEmpty) {
        controller = CameraController(cameras[0], ResolutionPreset.medium);
        controller.initialize().then((_) {
          if (!mounted) {
            return;
          }
          setState(() {});
        });
      }
    });
  }

  Future<void> captureAndSendImage() async {
    try {
      final image = await controller.takePicture();
      // Optionally, you can preview the image here

      // Send image to server
      sendImageToServer(image.path);
    } catch (e) {
      // Error handling
      print(e);
    }
  }

  Future<void> sendImageToServer(String imagePath) async {
    var uri = Uri.parse('http://yourserver.com/api/upload');
    var request = http.MultipartRequest('POST', uri)
      ..files.add(await http.MultipartFile.fromPath('image', imagePath));
    
    try {
      var response = await request.send();
      if (response.statusCode == 200) {
        // Success handling
      } else {
        // Error handling
      }
    } catch (e) {
      // Exception handling
      print(e);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (!controller.value.isInitialized) {
      return Center(child: CircularProgressIndicator());
    }
    if (controller == null || !controller.value.isInitialized) {
      return Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }
    return Scaffold(
      appBar: AppBar(title: Text('Capture Image')),
      body: CameraPreview(controller),
      floatingActionButton: FloatingActionButton(
        onPressed: captureAndSendImage,
        child: Icon(Icons.camera_alt),
      ),
    );
  }

  @override
  void dispose() {
    controller?.dispose();
    super.dispose();
  }
}

