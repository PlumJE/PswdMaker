# kivy/buildozer용 이미지 import
FROM kivy/buildozer:latest

# root가 아닌 계정으로 전환해서 안전하게 빌드 수행
USER user
WORKDIR /home/user/app

# 빌드
ENTRYPOINT ["buildozer"]
CMD ["-v", "android", "debug", "deploy", "run", "logcat"]