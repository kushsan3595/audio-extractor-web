# Setting Up Google AdSense for Your Audio Extractor Website

This guide will walk you through the process of creating a Google AdSense account and implementing ads on your Audio Extractor web application.

## Step 1: Deploy Your Website

Before applying for AdSense, make sure your website is:
1. Live on the internet with its own domain name
2. Has substantial original content
3. Complies with Google AdSense policies
4. Has a privacy policy page

## Step 2: Create a Google AdSense Account

1. Go to [Google AdSense](https://www.google.com/adsense/start/)
2. Click "Get Started" or "Sign up now"
3. Sign in with your Google account
4. Fill in your website URL and other required information
5. Accept the AdSense terms and conditions
6. Submit your application

Google will review your application, which may take a few days to a couple of weeks.

## Step 3: Verify Your Website

After submitting your application, Google will provide you with a verification code. You'll need to add this code to your website to verify ownership.

1. Add the code to your website by editing the `layout.html` file:

```html
<!-- Replace the existing AdSense code in the head section with the code Google provides -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-YOUR_PUBLISHER_ID"
     crossorigin="anonymous"></script>
```

2. Deploy the updated website
3. Wait for Google to verify your site (usually within a few days)

## Step 4: Set Up Your Ad Units

Once your account is approved:

1. Log in to your AdSense account
2. Go to "Ads" → "By ad unit"
3. Click "Create new ad unit"
4. Choose the ad format (display, in-article, etc.)
5. Configure your ad settings and get your ad code

## Step 5: Update Your Website with Real Ad Codes

Replace the placeholder ad codes in your templates with the actual codes from your AdSense account:

1. Open `templates/layout.html`
2. Replace `YOUR_PUBLISHER_ID` with your actual publisher ID
3. Replace `YOUR_AD_SLOT_ID` and `YOUR_AD_SLOT_ID_2` with the ad slot IDs you created
4. Deploy the updated website

Example:
```html
<!-- Replace this: -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-YOUR_PUBLISHER_ID"
     data-ad-slot="YOUR_AD_SLOT_ID"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>

<!-- With your actual AdSense code: -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-1234567890123456"
     data-ad-slot="7891234567"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
```

## Step 6: Ad Placement Best Practices

For optimal performance:

1. Place ads where they're visible but not intrusive
2. Don't overload your pages with too many ads
3. Test different ad placements to see what works best
4. Ensure ads don't interfere with your application's functionality

## Step 7: Monitor Performance

After implementing the ads:

1. Monitor your AdSense dashboard for performance metrics
2. Check that the ads are displaying correctly on different devices
3. Make adjustments as needed to improve performance

## Important Notes

- **Policy Compliance**: Always comply with [Google AdSense program policies](https://support.google.com/adsense/answer/48182)
- **Content Guidelines**: Ensure your website has sufficient unique content
- **User Experience**: Maintain a good balance between content and ads
- **Invalid Traffic**: Never click on your own ads or encourage others to do so

## Troubleshooting

If your ads aren't displaying:
1. Check the browser console for errors
2. Verify your ad code is implemented correctly
3. Make sure your account is approved and active
4. Check for any policy violations in your AdSense account

For more help, visit the [Google AdSense Help Center](https://support.google.com/adsense). 