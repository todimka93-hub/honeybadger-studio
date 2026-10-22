# ASYA: новые ролики без перезаписи старых

Открыть генератор: https://colab.research.google.com/github/todimka93-hub/honeybadger-studio/blob/main/colab/any_animal_10_images.ipynb

1. В Colab выбери PROJECT = "crow", "wolverine" или "wolf". Для нового животного добавь ключ, style и 10 scenes в корневой projects.json.
2. Выполни ячейки генерации на GPU (если доступен).
3. При желании выполни последнюю ячейку, чтобы отправить 10 PNG в projects/PROJECT/assets/ через GitHub token.
4. Добавь озвучку voice.mp3 в projects/PROJECT/assets/.
5. GitHub Actions → Build Project → Run workflow → project: PROJECT. Если озвучка уже была загружена перед изображениями, ноутбук попытается запустить сборку сам.
6. Скачай MP4 в Artifacts. Каждый проект сохраняет собственные материалы и не стирает другие.

Внимание: бесплатный Colab GPU не гарантирован. SD-Turbo даёт относительно низкое качество. Генерация и загрузка пока требуют ручного запуска ноутбука и токена; полностью автономного ChatGPT-агента здесь нет. Видео использует одинаковое время для каждой сцены, а не синхронизацию по смысловым фразам.
