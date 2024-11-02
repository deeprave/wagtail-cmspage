const SOCIAL_NAMES = {
  "discord": "Discord",
  "envelope": "Email",
  "facebook": "Facebook",
  "github": "GitHub",
  "instagram": "Instagram",
  "linkedin": "LinkedIn",
  "medium": "Medium",
  "facebook-messenger": "Messenger",
  "pinterest": "Pinterest",
  "reddit": "Reddit",
  "rss": "RSS",
  "skype": "Skype",
  "slack": "Slack",
  "snapchat": "Snapchat",
  "telegram": "Telegram",
  "tiktok": "TikTok",
  "tumblr": "Tumblr",
  "twitch": "Twitch",
  "twitter": "Twitter",
  "vimeo": "Vimeo",
  "whatsapp": "WhatsApp",
  "X": "X",
  "youtube": "YouTube",
  "zoom": "Zoom"
}

class SocialLinkBlockDefinition extends window.wagtailStreamField.blocks.StructBlockDefinition {

  render(placeholder, prefix, initialState, initialError) {
    const block = super.render(
        placeholder,
        prefix,
        initialState,
        initialError,
    )

    const iconSelect = document.getElementById(prefix + "-icon")
    const nameInput = document.getElementById(prefix + "-name")
    const updateNameInput = () => {
        nameInput.value = SOCIAL_NAMES[iconSelect.value] || ''
    }
    updateNameInput()
    iconSelect.addEventListener('change', updateNameInput)
    return block
  }
}

window.telepath.register('cmspage.blocks.SocialLinkBlock', SocialLinkBlockDefinition)
