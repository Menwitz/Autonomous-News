# News Autonomous Platform

## Features

- **Scraping News Headlines**: Uses AWS Lambda to scrape news headlines from 100 websites twice a day.
- **Generating Articles**: Uses the OpenAI API to generate detailed articles based on the headlines.
- **Paraphrasing Articles**: Paraphrases the generated articles to make them more natural and human-like.
- **Editor Review**: Provides a web-based editor interface for reviewing, editing, and enhancing articles with images.
- **SEO Optimization**: Automatically optimizes articles for SEO.
- **Publishing to WordPress**: Publishes the finalized articles to a WordPress site.
- **Social Media Integration**: Automatically shares published articles on social media platforms.

## Project Structure

news-autonomous-platform/
├── README.md
├── LICENSE
├── .gitignore
├── infrastructure/
│   ├── cloudformation/
│   │   ├── templates/
│   │   │   ├── dynamodb.yaml
│   │   │   ├── s3.yaml
│   │   │   ├── lambda.yaml
│   │   │   ├── ses.yaml
│   │   │   ├── cloudwatch.yaml
│   │   │   ├── sns.yaml
│   │   ├── deploy.sh
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── provider.tf
├── lambdas/
│   ├── scrape_news/
│   │   ├── scrape_news.py
│   │   ├── requirements.txt
│   ├── generate_article/
│   │   ├── generate_article.py
│   │   ├── requirements.txt
│   ├── paraphrase_article/
│   │   ├── paraphrase_article.py
│   │   ├── requirements.txt
│   ├── publish_article/
│   │   ├── publish_article.py
│   │   ├── requirements.txt
│   ├── post_to_social_media/
│   │   ├── post_to_social_media.py
│   │   ├── requirements.txt
│   ├── optimize_seo/
│   │   ├── optimize_seo.py
│   │   ├── requirements.txt
├── web-editor/
│   ├── public/
│   │   ├── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── ArticleEditor.js
│   │   │   ├── ArticleList.js
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── aws-exports.js
│   ├── package.json
│   ├── package-lock.json
│   ├── .env.example
├── scripts/
│   ├── notify_editor.py
│   ├── email_templates/
│   │   ├── new_article_notification.html
└── docs/
    ├── architecture.md
    ├── setup_guide.md
    ├── usage_guide.md
    ├── contributing.md



### Prerequisites

- AWS Account
- Node.js and npm
- Python 3.x
- AWS CLI configured
- OpenAI API key

### Setup Guide

Follow the steps in the [setup guide](docs/setup_guide.md) to configure and deploy the project.

### Usage

Refer to the [usage guide](docs/usage_guide.md) for detailed instructions on how to use the platform.

### Contributing

Read the [contributing guide](docs/contributing.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

