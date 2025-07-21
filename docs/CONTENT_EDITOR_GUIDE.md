# Content Editor Guide

**A complete guide for content creators using wagtail-cmspage**

This guide is designed for content editors, marketing teams, and anyone who creates and manages content using wagtail-cmspage in the Wagtail admin interface. No technical knowledge is required!

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Creating Your First CMS Page](#creating-your-first-cms-page)
3. [Understanding Content Blocks](#understanding-content-blocks)
4. [Page Settings & SEO](#page-settings--seo)
5. [Preview & Publishing](#preview--publishing)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

## 🚀 Getting Started

### Accessing the Admin Interface

1. **Login to Wagtail Admin** - Navigate to your site's admin URL (usually `/admin/`)
2. **Go to Pages** - Click "Pages" in the main navigation
3. **Find your section** - Navigate to where you want to create content

### Understanding the Interface

The Wagtail admin interface has several key areas:
- **Pages tree** - Hierarchical view of all pages on your site
- **Page editor** - Where you create and edit content
- **Preview panel** - Shows how your page will look to visitors
- **Publishing controls** - Manage page status and publication

## 📄 Creating Your First CMS Page

### Step 1: Add a New Page

1. Navigate to the parent page where you want to add content
2. Click **"Add child page"**
3. Select **"CMS Page"** from the list of page types
4. You'll be taken to the page editor

### Step 2: Basic Page Information

Fill in the essential page details:

**Page Title**
- This appears in browser tabs and search results
- Keep it descriptive but concise (under 60 characters)
- Example: "About Our Company" or "Product Features"

**Display Title Toggle**
- Check this box to show the title on the page itself
- Uncheck if you want the title only for navigation/SEO

**Page Tags**
- Add relevant keywords to help organize and find your content
- Use tags like "marketing", "product", "news", etc.
- Check "Display tags" if you want visitors to see them

### Step 3: SEO Settings

Click the **"Promote"** tab to set up SEO:

**SEO Title**
- How your page appears in search engine results
- Should be compelling and include important keywords
- If left blank, uses the page title

**SEO Keywords**
- Relevant keywords for search engines
- Separate multiple keywords with commas
- Example: "software, productivity, business tools"

**Meta Description**
- Brief description for search results (under 160 characters)
- Should entice people to click on your page

## 🧩 Understanding Content Blocks

CMS Pages use a flexible block system. Click **"+ Add"** to add content blocks:

### 🎨 Universal Styling Options

Most content blocks include these styling options:

#### **Palette (Color Themes)**
Controls the background and text colors of your block:

- **Transparent Background** - No background color (default)
- **Page Theme (respects light/dark mode)** - Matches your site's main theme, adapts automatically
- **Light Theme (fixed light)** - Always uses light colors (white background, dark text)
- **Dark Theme (fixed dark)** - Always uses dark colors (dark background, light text)
- **Black on White** - Pure white background with black text
- **White on Black** - Pure black background with white text
- **Highlight Theme (alternate background)** - Uses your site's accent color for highlights
- **Standout Theme (secondary alternate)** - Secondary highlight color for variety
- **Success (green for positive actions)** - Green theme for positive messages, confirmations
- **Warning (yellow for caution)** - Yellow/orange theme for cautions and important notices
- **Info (using site palette colors)** - Blue theme for informational content
- **Danger (red for errors/critical)** - Red theme for alerts, errors, or critical messages

#### **Inset (Spacing)**
Adds padding (white space) around your content:

- **None** - No extra spacing
- **Small (responsive)** - Minimal padding, automatically adjusts for mobile
- **Medium (responsive)** - Comfortable padding, automatically adjusts for mobile
- **Large (responsive)** - Generous padding, automatically adjusts for mobile
- **Larger (responsive)** - Very generous padding, automatically adjusts for mobile
- **Largest (responsive)** - Maximum padding, automatically adjusts for mobile

*All inset options automatically provide more spacing on larger screens and less on mobile devices*

#### **Image Options** (for blocks with images)

**Size:**
- **Tiny** - Very small display
- **Small** - Compact display
- **Medium** - Standard size
- **Large** - Prominent display
- **Full Width** - Spans the full width of the container
- **Original** - Uses the original image size

**Orientation:**
- **Landscape** - Wide, horizontal crop (good for scenery/banners)
- **Portrait** - Tall, vertical crop (good for people/products)
- **Square** - Equal width/height (consistent grid layouts)
- **Extra Wide** - Very wide horizontal crop

**Rounding:**
- **None (-1)** - Sharp corners
- **0** - Minimal rounding
- **1** - Slight rounding
- **2** - Moderate rounding
- **3** - More rounded corners
- **4** - Very rounded corners
- **5** - Maximum rounding (nearly circular)

**Responsive Toggle:**
- **On** - Image size adjusts automatically on mobile
- **Off** - Image maintains fixed size across devices

**Crop Tool:**
- Click and drag to select the most important part of your image
- This area will always stay visible when image is resized

### 🌈 Working with Palettes and Themes

#### **Palette Best Practices:**

**For Standard Content:**
- Use **"Page"** for most content blocks - it adapts to your site's theme
- Choose **"Transparent"** when you don't need background colors

**For Special Sections:**
- **"Accent"** - Highlight important features or call-to-action sections
- **"Light"** - Create bright, clean sections that stand out
- **"Dark"** - Add dramatic contrast or create focus areas
- **"Card"** - Give content a subtle, contained appearance

**For Status Messages:**
- **"Success"** - Positive news, achievements, confirmations
- **"Warning"** - Important notices, cautions
- **"Info"** - Helpful information, tips
- **"Danger"** - Alerts, errors, urgent messages

**For Brand Consistency:**
- **"White"** - Pure white sections for minimalist design
- **"Black"** - Bold, dramatic sections
- **"Emphasis"** - Strong contrast for key messaging

#### **Theme Switching Support:**
Your site supports automatic light/dark theme switching. When you choose:
- **"Page"** palette - Automatically adapts to visitor's theme preference
- **"Light"** palette - Always appears light, regardless of theme
- **"Dark"** palette - Always appears dark, regardless of theme

**💡 Pro Tip:** Preview your page in both light and dark modes using the theme switcher (sun/moon icons) to ensure your content looks good in all conditions.

### Hero Image Block
**Perfect for:** Page headers, feature announcements

**What it does:** Creates a large, prominent image display

**How to use:**
1. **Upload Image** - Choose a high-quality image (required)
2. **Configure Image Display:**
   - **Image orientation**: Landscape, Portrait, Square, or Extra Wide
   - **Image size**: Tiny, Small, Medium, Large, Full Width, or Original
   - **Crop percentage**: None (0), Small (25%), Medium (50%), Large (75%), Full (100%)
   - **Image rounding**: None (-1) through Maximum (5) for rounded corners
   - **Image responsive**: Checkbox for mobile optimization
3. **Styling Options:**
   - **Palette**: Choose color theme for background
   - **Padding around the block**: None through Largest for spacing

**Tips:**
- Use "Full Width" size for maximum impact banners
- Choose "Landscape" or "Extra Wide" orientation for page headers
- Enable "Image responsive" for mobile optimization
- Use "Large" or "Largest" padding for breathing room around the image

### Title Block
**Perfect for:** Section headings, page introductions

**What it does:** Creates styled headings with optional formatting

**How to use:**
1. **Enter Content:**
   - **Title text to display**: The main heading text (required)
2. **Text Formatting:**
   - **Use the cursive font on title?**: Checkbox for decorative font
   - **Title text alignment**: Left, Center, or Right (defaults to Center)
3. **Styling Options:**
   - **Palette**: Choose color theme for background
   - **Padding around the block**: None through Largest for spacing

**Tips:**
- Use cursive font for elegant, decorative headings
- Center alignment works well for section titles
- Choose "Page Theme" palette to match your site's design
- Use "Medium" or "Large" padding for section breaks
- Keep titles concise and descriptive

### Rich Text Block
**Perfect for:** Articles, detailed descriptions, formatted content

**What it does:** Provides full text editing with optional title and formatting options

**How to use:**
1. **Enter Content:**
   - **Display title, optional (max len=120)**: Optional heading for the section
   - **Rich text block, required**: Main content with toolbar for formatting (bold, italic, lists, links, etc.)
2. **Text Formatting:**
   - **Use the cursive font on title?**: Checkbox for decorative font on title
   - **Text alignment**: Left, Center, or Right for the entire block
3. **Styling Options:**
   - **Palette**: Choose color theme for background
   - **Padding around the block**: None through Largest for spacing

**Tips:**
- Use the optional title to introduce your content section
- Break up long text with headings and lists using the rich text toolbar
- Use bullet points for easy scanning
- Add internal links to related pages using the link tool
- Choose "Page Theme" palette for standard content
- Add "Medium" padding for better readability around text blocks

### Cards Block
**Perfect for:** Feature lists, team members, product showcases

**What it does:** Creates responsive card layouts

**How to use:**
1. **Add Cards:**
   - Click "Add card" to create each card
   - **Card Title**: Bold title text (max 255 characters)
   - **Card Text**: Optional rich text content
   - **Card Image**: Optional image for each card
   - **Card Link**: Optional page, document, or external link
2. **Configure Each Card:**
   - **Text alignment**: Left, Center, or Right for card content
   - **Image orientation**: Landscape, Portrait, Square, or Extra Wide
   - **Image size**: Tiny, Small, Medium, Large, Full Width, or Original
   - **Crop percentage**: None (0) through Full (100%)
   - **Image responsive**: Checkbox for mobile optimization
   - **Card palette**: Individual color theme for each card
   - **Padding around the card**: Individual spacing for each card
3. **Block-Level Options:**
   - **Use the cursive font in titles?**: Apply decorative font to all card titles
   - **Image rounding**: Universal rounding level for all card images (None through Maximum)
4. **Overall Styling:**
   - **Palette**: Background theme for the entire cards block
   - **Padding around the block**: Spacing around the entire set of cards

**Tips:**
- Keep card content consistent in length
- Use "Square" orientation with "Medium" rounding for team photos
- Choose "Card" palette for subtle card backgrounds
- Use "Small" padding for compact layouts, "Medium" for comfortable spacing
- Limit to 3-6 cards for best visual impact
- Enable responsive toggle for mobile optimization

### Image & Text Block
**Perfect for:** Feature explanations, about sections

**What it does:** Places text alongside or overlaid on an image

**How to use:**
1. **Add Content:**
   - **Title**: Optional title text (max 60 characters)
   - **Text**: Optional rich text content
   - **Image**: Upload your image
2. **Configure Image Display:**
   - **Image orientation**: Landscape, Portrait, Square, or Extra Wide
   - **Image size**: Tiny, Small, Medium, Large, Full Width, or Original
   - **Crop percentage**: None (0) through Full (100%)
   - **Image rounding**: None (-1) through Maximum (5)
   - **Image responsive**: Checkbox for mobile optimization
3. **Layout Options:**
   - **Image left - text right, or image right - text left**: Choose image position (Left, Right, Center, Full)
   - **Overlay text on image**: Checkbox to place text over the image instead of beside it
4. **Text Formatting:**
   - **Use the cursive font on title?**: Checkbox for decorative title font
   - **Block text alignment**: Left, Center, or Right
5. **Styling Options:**
   - **Palette**: Background color theme
   - **Padding around the block**: None through Largest for spacing
   - **Link**: Optional page, document, or external link

**Tips:**
- Use "Portrait" or "Square" orientation for better mobile display
- Choose "Medium" or "Large" size for feature sections
- Enable "Overlay text on image" for dramatic hero-style layouts
- Keep text concise and focused when using overlay
- Alternate image positions for visual variety
- Use "Accent" palette to highlight important features
- Add "Medium" padding for comfortable spacing

### Call-to-Action Block
**Perfect for:** Contact forms, sign-ups, downloads

**What it does:** Creates prominent action sections with optional button links

**How to use:**
1. **Add Content:**
   - **Title**: Optional compelling headline (max 60 characters)
   - **Call to action text**: Optional description text above button (max 200 characters)
   - **Link**: Configure button destination (page, document, or external link)
2. **Text Formatting:**
   - **Use the cursive font?**: Checkbox for decorative title font
   - **Text alignment**: Left, Center, or Right for all content
3. **Button Configuration:**
   - **Button Title**: Text for the action button (use hyphen for special link button)
   - **Page link**: Link to internal page
   - **Document link**: Link to downloadable file
   - **Extra link**: External URL
4. **Block Styling:**
   - **CTA Button palette**: Color theme for the button and block background
   - **Padding around the block**: None through Largest for spacing

**Tips:**
- Use action-oriented button text ("Get Started", "Learn More", "Download Now")
- Choose "Warning" or "Success" palette to make CTAs stand out
- Use "Large" padding for important calls-to-action
- Keep title and description text concise and compelling
- Make sure links work and go to the right place
- Use sparingly for maximum impact

### Table Block
**Perfect for:** Pricing, comparisons, data presentation

**What it does:** Creates formatted tables with Wagtail's built-in table editor

**How to use:**
1. **Configure Table:**
   - Use the table editor to set number of rows and columns
   - Fill in table data using the interactive editor
   - Mark header rows/columns as needed
   - Built-in table editing with add/remove rows and columns
2. **Block Styling:**
   - **Palette**: Background theme for the table container
   - **Padding around the block**: Spacing around the entire table

**Tips:**
- Keep tables simple and readable
- Use headers to explain data
- Tables automatically include responsive behavior
- Choose "Light" or "Card" palette for subtle container backgrounds
- Add "Small" padding for clean presentation
- Consider cards or lists for mobile-friendly alternatives when tables get complex
- Test on mobile devices to ensure readability

### Carousel Block
**Perfect for:** Image galleries, product photos

**What it does:** Creates sliding image galleries with automatic transitions

**How to use:**
1. **Add Carousel Items:**
   - Click "Add carousel" to create each slide
   - **Carousel image**: Upload image for each slide (required)
   - **Display title, optional (max len=120)**: Optional heading for each slide
   - **Short description**: Optional text content (max 256 characters)
   - **Attribution, optional (max len=80)**: Optional image credit or caption
2. **Configure Each Slide:**
   - **Text alignment**: Left, Center, or Right for slide text content
3. **Carousel Settings:**
   - **Keep visible for time in milliseconds**: Auto-advance timing (default: 12000ms = 12 seconds)
4. **Block Styling:**
   - **Palette**: Background theme for the entire carousel
   - **Padding around the block**: Spacing around the carousel container

**Tips:**
- Use images of similar dimensions and orientation for best results
- Keep slide titles and descriptions concise
- Provide attribution for stock photos or external images
- Don't make carousels too long (5-8 images max for user attention)
- Use 8-15 second intervals for comfortable reading time
- Choose "Page" or "Light" palette for neutral gallery backgrounds
- Add "Medium" padding for comfortable spacing around the carousel

### Form Block
**Perfect for:** Contact forms, surveys, feedback

**What it does:** Creates custom forms with various field types and validation

**How to use:**
1. **Form Setup:**
   - **Form title displayed at the top**: Main heading for your form (required)
   - **Description of the form's purpose**: Optional explanatory text
   - **URL to which the form data is to be submitted**: Where form data goes (required)
   - **Submit button text**: Button label (default: "Submit")
   - **Success message**: Message shown after successful submission (default: "Form submitted successfully")
2. **Add Form Fields:**
   - **Text Field**: Basic text input with label and help text
   - **Textarea Field**: Multi-line text input
   - **Email Field**: Email address input with validation
   - **Integer Field**: Number input for whole numbers
   - **Decimal Field**: Number input for decimal values
   - **Select Field**: Dropdown menu with predefined options
   - **Multiselect Field**: Multiple choice selection
3. **Configure Each Field:**
   - **Label**: What users see for the field (required)
   - **Help text**: Optional guidance for users
   - **Required**: Whether the field must be filled
   - **Default value**: Pre-filled content (where applicable)

**Tips:**
- Keep forms short and focused on essential information
- Use clear, descriptive field labels
- Provide helpful guidance in help text fields
- Mark required fields appropriately
- Test form submission thoroughly before publishing
- Use email field type for email addresses to get built-in validation
- Choose descriptive success messages that confirm the action taken

## ⚙️ Page Settings & SEO

### Content Tab
- **Page title** - Main page name
- **Tags** - Help organize and categorize content
- **Display options** - Control what appears on the page

### Promote Tab
- **SEO title** - Search engine title (60 characters max)
- **Meta description** - Search result description (160 characters max)
- **Keywords** - Relevant search terms

### Settings Tab
- **Slug** - URL-friendly page name (auto-generated from title)
- **Go live date** - When page becomes public
- **Expiry date** - When page is automatically unpublished

## 👀 Preview & Publishing

### Preview Your Work
1. Click **"Preview"** to see how your page looks
2. Test on different devices using the device toolbar
3. Check both light and dark themes if theme switching is enabled
4. Verify all links and buttons work correctly

### Publishing Options

**Save Draft**
- Saves your work without making it public
- Allows continued editing
- Use while content is in progress

**Publish**
- Makes your page live immediately
- Visible to all website visitors
- Use when content is final and ready

**Schedule Publishing**
- Set a future date/time for publication
- Useful for time-sensitive content
- Content remains draft until scheduled time

**Unpublish**
- Removes page from public view
- Content remains in system for future editing
- Use for outdated or temporary removal

## ✅ Best Practices

### Content Strategy
- **Plan your page structure** before adding blocks
- **Use consistent styling** across similar pages
- **Test on mobile devices** - most visitors use phones
- **Keep accessibility in mind** - use descriptive alt text for images

### Writing Tips
- **Write for your audience** - use their language and tone
- **Front-load important information** - put key points first
- **Use active voice** - "We help businesses grow" vs "Businesses are helped"
- **Include calls-to-action** - tell visitors what to do next

### Image Guidelines
- **Use high-quality images** - crisp, well-lit, professional
- **Optimize file sizes** - compress images to load faster
- **Add alt text** - describe images for accessibility
- **Maintain brand consistency** - use consistent styles and colors

### SEO Best Practices
- **Use descriptive page titles** with important keywords
- **Write compelling meta descriptions** that encourage clicks
- **Structure content with headings** (H1, H2, H3...)
- **Link to related content** within your site

## 🔧 Troubleshooting

### Common Issues

**"My changes aren't showing"**
- Make sure you clicked "Publish" not just "Save Draft"
- Try refreshing the page or clearing browser cache
- Check if you're viewing the correct page URL

**"Images aren't displaying"**
- Verify image file formats (JPEG, PNG, WebP are best)
- Check file sizes aren't too large (under 2MB recommended)
- Ensure images uploaded successfully

**"Links aren't working"**
- Check URLs are complete (include http:// or https://)
- For internal links, use the page chooser when possible
- Test links in preview mode

**"Form submissions aren't working"**
- Verify the submit URL is correct
- Check that all required fields are filled
- Contact your site administrator if issues persist

### Getting Help

**Preview Everything**
- Always preview your work before publishing
- Test on different screen sizes
- Check all interactive elements

**Ask for Review**
- Have colleagues review important pages
- Get feedback on clarity and effectiveness
- Use Wagtail's workflow features if available

**Contact Support**
- Keep error messages or screenshots handy
- Note what you were trying to do when issues occurred
- Include page URLs and browser information

---

## 🎯 Quick Reference

### Essential Keyboard Shortcuts
- **Ctrl/Cmd + S** - Save draft
- **Ctrl/Cmd + Enter** - Publish page
- **Escape** - Close modals/panels

### Block Selection Guide
- **Page header** → Hero Image
- **Main content** → Rich Text
- **Features/services** → Cards
- **Explanations** → Image & Text
- **Contact/signup** → Call-to-Action
- **Data/pricing** → Table
- **Photo gallery** → Carousel
- **Contact form** → Form

### File Size Guidelines
- **Images**: Under 2MB, 1200px+ width for heroes
- **Files**: Under 10MB for downloads
- **Videos**: Use external hosting (YouTube, Vimeo)

---

**Happy content creating! 🎉**

*This guide covers the basics of content creation with wagtail-cmspage. For technical implementation details, see the [Developer Reference](CMSPAGE.md).*
