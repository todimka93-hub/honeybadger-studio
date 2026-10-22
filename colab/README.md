# Бесплатная генерация 10 отдельных изображений

Открыть ноутбук: https://colab.research.google.com/github/todimka93-hub/honeybadger-studio/blob/main/colab/crow_10_images.ipynb

1. В Colab включить GPU T4 (если доступен бесплатно).
2. Нажать Runtime → Run all.
3. Дождаться скачивания crow_10_independent_scenes.zip.
4. Распаковать scene_01.png … scene_10.png в assets/ репозитория и добавить voice.mp3, затем запустить Build Shorts.

Изображения генерируются **по одному независимо**. Модель SD-Turbo 512×768, увеличение до 1080×1920 не увеличивает исходную детализацию. Без GPU не запустится. Бесплатный GPU Colab не гарантирован.