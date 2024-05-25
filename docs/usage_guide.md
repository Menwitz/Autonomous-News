# Usage Guide

This guide provides instructions on how to use the autonomous news platform.

## Scraping News Headlines

The platform automatically scrapes news headlines twice a day. To manually trigger the scraping process, you can invoke the `scrape_news` Lambda function from the AWS Management Console or CLI.

```bash
aws lambda invoke --function-name scrape_news output.txt
```

## Generating Articles

Articles are generated based on the scraped headlines. To manually trigger article generation, invoke the `generate_article` Lambda function.

```bash
aws lambda invoke --function-name generate_article output.txt
```

## Paraphrasing Articles

Articles are paraphrased to make them more natural and human-like. To manually trigger paraphrasing, invoke the `paraphrase_article` Lambda function.

```bash
aws lambda invoke --function-name paraphrase_article output.txt
```

## Editor Review

Editors can review and edit articles using the web-based interface. The interface provides a rich text editor and options to upload images.

1. **Navigate to the Web Editor**

   Open the web editor URL in your browser.

2. **Log In**

   Log in with your credentials.

3. **Review Articles**

   Select an article from the list and review its content.

4. **Edit Articles**

   Use the editor to make changes to the article. Upload images if necessary.

5. **Save Changes**

   Save your changes. The edited article will be stored in S3.

## SEO Optimization

Articles are automatically optimized for SEO before publication. To manually trigger SEO optimization, invoke the `optimize_seo` Lambda function.

```bash
aws lambda invoke --function-name optimize_seo output.txt
```

## Publishing Articles

Articles are published to a WordPress site. To manually trigger publication, invoke the `publish_article` Lambda function.

```bash
aws lambda invoke --function-name publish_article output.txt
```

## Social Media Integration

Published articles are shared on social media platforms. To manually trigger social media posting, invoke the `post_to_social_media` Lambda function.

```bash
aws lambda invoke --function-name post_to_social_media output.txt
```

## Monitoring and Logging

The platform uses CloudWatch for monitoring and logging. You can view logs and set up alerts in the AWS Management Console.

## Troubleshooting

If you encounter any issues, check the CloudWatch logs for the corresponding Lambda function. Ensure that all AWS resources are correctly configured and that your environment variables are set up properly.
