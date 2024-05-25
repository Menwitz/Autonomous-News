# Architecture

This document provides an overview of the architecture for the autonomous news platform.

## Overview

The platform is designed to autonomously scrape news headlines, generate articles, paraphrase content, allow editor review, optimize for SEO, and publish to a WordPress site. It leverages various AWS services and integrates with the OpenAI API for content generation.

## Components

### AWS Lambda

- **Scrape News Headlines**: Scrapes news headlines from a list of websites.
- **Generate Articles**: Uses the OpenAI API to generate articles based on the headlines.
- **Paraphrase Articles**: Paraphrases the generated articles.
- **Notify Editors**: Sends email notifications to editors.
- **SEO Optimization**: Optimizes articles for SEO.
- **Publish Articles**: Publishes articles to WordPress.
- **Post to Social Media**: Shares published articles on social media.

### AWS S3

- **Storage for Articles**: Stores paraphrased and edited articles.
- **Storage for Images**: Stores images uploaded by editors.

### AWS DynamoDB

- **NewsHeadlines Table**: Stores scraped news headlines.
- **GeneratedArticles Table**: Stores generated articles and their metadata.

### AWS SES

- **Email Notifications**: Sends email notifications to editors about new articles.

### AWS SNS

- **Notification System**: Manages notifications for new articles.

### AWS CloudWatch

- **Monitoring and Logging**: Monitors the Lambda functions and logs their execution.

### Web-Based Editor

- **Editor Interface**: Provides an interface for editors to review and edit articles.
- **Built with React**: Developed using React and hosted on AWS.

## Data Flow

1. **Scrape News Headlines**: Lambda function scrapes news headlines and stores them in DynamoDB.
2. **Generate Articles**: Lambda function generates articles using OpenAI and stores them in DynamoDB.
3. **Paraphrase Articles**: Lambda function paraphrases articles and stores them in S3.
4. **Notify Editors**: SES sends email notifications to editors.
5. **Editor Review**: Editors review and edit articles using the web-based interface.
6. **SEO Optimization**: Lambda function optimizes articles for SEO.
7. **Publish Articles**: Lambda function publishes articles to WordPress.
8. **Social Media Integration**: Lambda function posts articles to social media.

## Diagram

![Architecture Diagram](architecture-diagram.png)

