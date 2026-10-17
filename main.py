name: Build Android APK

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libffi-dev libssl-dev

    - name: Install Buildozer and Cython
      run: |
        python -m pip install --upgrade pip
        pip install --upgrade cython buildozer

    - name: Build with Buildozer
      run: |
        buildozer init
        sed -i 's/#title = My Application/title = MyGame/g' buildozer.spec
        sed -i 's/#package.name = myapp/package.name = mygame/g' buildozer.spec
        sed -i 's/#package.domain = org.test/package.domain = org.game/g' buildozer.spec
        yes | buildozer -v android debug

    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: android-apk
        path: bin/*.apk
