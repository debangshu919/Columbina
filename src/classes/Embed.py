"""
Custom Discord Embed classes for consistent styling across the bot.
"""

from datetime import datetime
from typing import Optional

import discord

from configs.config import CONFIG


def _rgb_to_color(rgb_list: list[int]) -> discord.Color:
    """Convert RGB list from config to discord.Color."""
    return discord.Color.from_rgb(rgb_list[0], rgb_list[1], rgb_list[2])


class BaseEmbed(discord.Embed):
    """
    Base embed class with common functionality.
    Extend this class for specific embed types.
    """

    def __init__(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        color: Optional[discord.Color] = None,
        timestamp: Optional[datetime] = None,
        show_timestamp: bool = False,
        footer_text: Optional[str] = None,
        footer_icon: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        image_url: Optional[str] = None,
        author_name: Optional[str] = None,
        author_icon: Optional[str] = None,
        author_url: Optional[str] = None,
        **kwargs,
    ):
        # Set timestamp if requested
        if show_timestamp and timestamp is None:
            timestamp = datetime.now()

        super().__init__(
            title=title,
            description=description,
            color=color,
            timestamp=timestamp,
            **kwargs,
        )

        # Set footer if provided
        if footer_text:
            self.set_footer(text=footer_text, icon_url=footer_icon)

        # Set thumbnail if provided
        if thumbnail_url:
            self.set_thumbnail(url=thumbnail_url)

        # Set image if provided
        if image_url:
            self.set_image(url=image_url)

        # Set author if provided
        if author_name:
            self.set_author(name=author_name, icon_url=author_icon, url=author_url)


class ErrorEmbed(BaseEmbed):
    """
    Error embed with red styling for error messages.

    Usage:
        # Basic error with default message
        embed = ErrorEmbed()

        # Custom error message
        embed = ErrorEmbed(error="User not found!")

        # With title and additional context
        embed = ErrorEmbed(
            title="Permission Denied",
            error="You don't have permission to use this command."
        )

        # With all options
        embed = ErrorEmbed(
            title="Database Error",
            error="Failed to save settings.",
            show_timestamp=True,
            footer_text="Please try again later"
        )

        # Quick factory methods
        embed = ErrorEmbed.permission_denied()
        embed = ErrorEmbed.not_found("User")
        embed = ErrorEmbed.invalid_input("Please provide a valid number.")
    """

    DEFAULT_ERROR = "Something went wrong."
    DEFAULT_TITLE = "Error"

    def __init__(
        self,
        error: Optional[str] = None,
        title: Optional[str] = None,
        show_timestamp: bool = False,
        footer_text: Optional[str] = None,
        footer_icon: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        suggestion: Optional[str] = None,
        **kwargs,
    ):
        """
        Create an error embed.

        Args:
            error: Custom error message. Defaults to "Something went wrong."
            title: Embed title. Defaults to "Error" if error is provided.
            show_timestamp: Whether to show timestamp. Defaults to False.
            footer_text: Optional footer text.
            footer_icon: Optional footer icon URL.
            thumbnail_url: Optional thumbnail URL.
            suggestion: Optional suggestion text that appears below the error.
        """
        # Build description
        description = error or self.DEFAULT_ERROR
        if suggestion:
            description += f"\n\n-# Hint: {suggestion}"

        # Set default title if error message is provided but title isn't
        if error and not title:
            title = self.DEFAULT_TITLE

        # Get error color from config
        error_color = _rgb_to_color(CONFIG["colors"]["error"])

        super().__init__(
            title=title,
            description=description,
            color=error_color,
            show_timestamp=show_timestamp,
            footer_text=footer_text,
            footer_icon=footer_icon,
            thumbnail_url=thumbnail_url,
            **kwargs,
        )

    # Factory methods for common error types
    @classmethod
    def permission_denied(cls, action: Optional[str] = None, **kwargs) -> "ErrorEmbed":
        """Create a permission denied error embed."""
        if action:
            error = f"You don't have permission to {action}."
        else:
            error = "You don't have permission to use this command."
        return cls(title="Permission Denied", error=error, **kwargs)

    @classmethod
    def not_found(cls, resource: str = "Resource", **kwargs) -> "ErrorEmbed":
        """Create a not found error embed."""
        return cls(
            title="Not Found",
            error=f"{resource} was not found.",
            **kwargs,
        )

    @classmethod
    def invalid_input(
        cls, message: str, suggestion: Optional[str] = None, **kwargs
    ) -> "ErrorEmbed":
        """Create an invalid input error embed."""
        return cls(
            title="Invalid Input",
            error=message,
            suggestion=suggestion,
            **kwargs,
        )

    @classmethod
    def timeout(cls, action: str = "operation", **kwargs) -> "ErrorEmbed":
        """Create a timeout error embed."""
        return cls(
            title="Timeout",
            error=f"The {action} timed out. Please try again.",
            **kwargs,
        )

    @classmethod
    def cooldown(cls, retry_after: float, **kwargs) -> "ErrorEmbed":
        """Create a cooldown error embed."""
        return cls(
            title="Cooldown",
            error=f"Please wait **{retry_after:.1f}** seconds before using this command again.",
            **kwargs,
        )

    @classmethod
    def internal_error(cls, **kwargs) -> "ErrorEmbed":
        """Create an internal error embed."""
        return cls(
            title="Internal Error",
            error="An unexpected error occurred. Please try again later.",
            footer_text="If this persists, please contact support.",
            **kwargs,
        )


class SuccessEmbed(BaseEmbed):
    """
    Success embed with green styling for success messages.

    Usage:
        # Basic success with default message
        embed = SuccessEmbed()

        # Custom success message
        embed = SuccessEmbed(message="Settings saved successfully!")

        # With title and additional context
        embed = SuccessEmbed(
            title="Configuration Complete",
            message="Your server has been configured successfully."
        )

        # With all options
        embed = SuccessEmbed(
            title="Welcome Setup",
            message="Welcome messages are now enabled!",
            show_timestamp=True,
            footer_text="Use /setup disable to turn off"
        )

        # Quick factory methods
        embed = SuccessEmbed.action_completed("banned", "User123")
        embed = SuccessEmbed.settings_saved()
    """

    DEFAULT_TITLE = "Success"

    def __init__(
        self,
        message: Optional[str] = None,
        title: Optional[str] = None,
        show_timestamp: bool = False,
        footer_text: Optional[str] = None,
        footer_icon: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        next_steps: Optional[str] = None,
        **kwargs,
    ):
        """
        Create a success embed.

        Args:
            message: Custom success message.
            title: Embed title. Defaults to "Success" if message is provided.
            show_timestamp: Whether to show timestamp. Defaults to False.
            footer_text: Optional footer text.
            footer_icon: Optional footer icon URL.
            thumbnail_url: Optional thumbnail URL.
            next_steps: Optional next steps text that appears below the message.
        """
        # Build description
        description = message
        if next_steps:
            description += f"\n\n📋 **Next Steps:** {next_steps}"

        # Set default title if message is provided but title isn't
        if message and not title:
            title = self.DEFAULT_TITLE

        # Get success color from config
        success_color = _rgb_to_color(CONFIG["colors"]["success"])

        super().__init__(
            title=title,
            description=description,
            color=success_color,
            show_timestamp=show_timestamp,
            footer_text=footer_text,
            footer_icon=footer_icon,
            thumbnail_url=thumbnail_url,
            **kwargs,
        )

    # Factory methods for common success types
    @classmethod
    def action_completed(
        cls, action: str, target: Optional[str] = None, **kwargs
    ) -> "SuccessEmbed":
        """Create an action completed success embed."""
        if target:
            message = f"Successfully {action} **{target}**."
        else:
            message = f"Successfully {action}."
        return cls(message=message, **kwargs)

    @classmethod
    def settings_saved(
        cls, setting_name: Optional[str] = None, **kwargs
    ) -> "SuccessEmbed":
        """Create a settings saved success embed."""
        if setting_name:
            message = f"**{setting_name}** settings have been saved."
        else:
            message = "Settings have been saved successfully."
        return cls(title="Settings Saved", message=message, **kwargs)

    @classmethod
    def feature_enabled(
        cls, feature: str, channel: Optional[str] = None, **kwargs
    ) -> "SuccessEmbed":
        """Create a feature enabled success embed."""
        message = f"**{feature}** has been enabled."
        if channel:
            message += f"\nChannel: {channel}"
        return cls(title="Feature Enabled", message=message, **kwargs)

    @classmethod
    def feature_disabled(cls, feature: str, **kwargs) -> "SuccessEmbed":
        """Create a feature disabled success embed."""
        return cls(
            title="Feature Disabled",
            message=f"**{feature}** has been disabled.",
            **kwargs,
        )

    @classmethod
    def welcome(cls, user_mention: str, server_name: str, **kwargs) -> "SuccessEmbed":
        """Create a welcome success embed."""
        return cls(
            title=f"Welcome to {server_name}!",
            message=f"Hey {user_mention}, we're glad to have you here!",
            **kwargs,
        )


class InfoEmbed(BaseEmbed):
    """
    Info embed with neutral styling for informational messages.

    Usage:
        embed = InfoEmbed(
            title="Server Information",
            message="Here are the server details..."
        )
    """

    def __init__(
        self,
        message: Optional[str] = None,
        title: Optional[str] = None,
        show_timestamp: bool = False,
        footer_text: Optional[str] = None,
        footer_icon: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        **kwargs,
    ):
        """
        Create an info embed.

        Args:
            message: Info message content.
            title: Embed title.
            show_timestamp: Whether to show timestamp. Defaults to False.
            footer_text: Optional footer text.
            footer_icon: Optional footer icon URL.
            thumbnail_url: Optional thumbnail URL.
        """

        # Get info color from config
        info_color = _rgb_to_color(CONFIG["colors"]["info"])

        super().__init__(
            title=title,
            description=message,
            color=info_color,
            show_timestamp=show_timestamp,
            footer_text=footer_text,
            footer_icon=footer_icon,
            thumbnail_url=thumbnail_url,
            **kwargs,
        )


class WarningEmbed(BaseEmbed):
    """
    Warning embed with orange/yellow styling for warning messages.

    Usage:
        embed = WarningEmbed(
            message="This action cannot be undone!",
            title="Confirm Deletion"
        )
    """

    DEFAULT_TITLE = "Warning"

    def __init__(
        self,
        message: Optional[str] = None,
        title: Optional[str] = None,
        show_timestamp: bool = False,
        footer_text: Optional[str] = None,
        footer_icon: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        **kwargs,
    ):
        """
        Create a warning embed.

        Args:
            message: Warning message content.
            title: Embed title. Defaults to "Warning" if message is provided.
            show_timestamp: Whether to show timestamp. Defaults to False.
            footer_text: Optional footer text.
            footer_icon: Optional footer icon URL.
            thumbnail_url: Optional thumbnail URL.
        """
        # Set default title if message is provided but title isn't
        if message and not title:
            title = self.DEFAULT_TITLE

        # Get warning color from config
        warning_color = _rgb_to_color(CONFIG["colors"]["warning"])

        super().__init__(
            title=title,
            description=message,
            color=warning_color,
            show_timestamp=show_timestamp,
            footer_text=footer_text,
            footer_icon=footer_icon,
            thumbnail_url=thumbnail_url,
            **kwargs,
        )


class PrimaryEmbed(BaseEmbed):
    """
    Primary embed using the bot's brand color.

    Usage:
        embed = PrimaryEmbed(
            title="About Columbina",
            message="I'm Columbina, a multi-purpose Discord bot..."
        )
    """

    def __init__(
        self,
        message: Optional[str] = None,
        title: Optional[str] = None,
        show_timestamp: bool = False,
        footer_text: Optional[str] = None,
        footer_icon: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        **kwargs,
    ):
        """
        Create a primary themed embed.

        Args:
            message: Message content.
            title: Embed title.
            show_timestamp: Whether to show timestamp. Defaults to False.
            footer_text: Optional footer text.
            footer_icon: Optional footer icon URL.
            thumbnail_url: Optional thumbnail URL.
        """
        # Get primary color from config
        primary_color = _rgb_to_color(CONFIG["colors"]["primary"])

        super().__init__(
            title=title,
            description=message,
            color=primary_color,
            show_timestamp=show_timestamp,
            footer_text=footer_text,
            footer_icon=footer_icon,
            thumbnail_url=thumbnail_url,
            **kwargs,
        )
