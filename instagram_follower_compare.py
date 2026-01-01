#!/usr/bin/env python3
"""
Instagram Follower Comparison Script

This script compares an Instagram user's follower list to their following list
and identifies users who are followed but don't follow back.

Usage:
    python instagram_follower_compare.py

The script expects to find 'followers.json' and 'following.json' in a
'followers_and_following' folder in the same directory.
"""

import json
import os
from pathlib import Path
from typing import Set, List, Dict, Any


def load_json_file(filepath: str) -> Any:
    """
    Load and parse a JSON file.

    Args:
        filepath: Path to the JSON file

    Returns:
        Parsed JSON data

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data


def extract_followers(data: List[Dict[str, Any]]) -> Set[str]:
    """
    Extract follower usernames from Instagram followers JSON.

    Format:
    [
        {
            "string_list_data": [
                {"value": "username", "timestamp": ...}
            ]
        },
        ...
    ]

    Args:
        data: Parsed JSON data from followers file

    Returns:
        Set of follower usernames
    """
    usernames = set()

    for entry in data:
        if "string_list_data" in entry:
            for item in entry["string_list_data"]:
                if "value" in item:
                    usernames.add(item["value"])

    return usernames


def extract_following(data: Dict[str, Any]) -> Set[str]:
    """
    Extract following usernames from Instagram following JSON.

    Format:
    {
        "relationships_following": [
            {
                "title": "username",
                "string_list_data": [...]
            },
            ...
        ]
    }

    Args:
        data: Parsed JSON data from following file

    Returns:
        Set of usernames the user is following
    """
    usernames = set()

    if "relationships_following" in data:
        for entry in data["relationships_following"]:
            if "title" in entry:
                usernames.add(entry["title"])

    return usernames


def find_non_followers(following: Set[str], followers: Set[str]) -> Set[str]:
    """
    Find users who are followed but don't follow back.

    Args:
        following: Set of usernames the user is following
        followers: Set of usernames who follow the user

    Returns:
        Set of usernames who don't follow back
    """
    return following - followers


def write_to_file(users: Set[str], output_path: str) -> None:
    """
    Write usernames to a text file, one per line, sorted alphabetically.

    Args:
        users: Set of usernames to write
        output_path: Path to the output file
    """
    sorted_users = sorted(users)

    with open(output_path, 'w', encoding='utf-8') as f:
        for user in sorted_users:
            f.write(f"{user}\n")


def main():
    """Main function to run the follower comparison."""
    print("Instagram Follower Comparison Script")
    print("=" * 40)

    # Define file paths
    script_dir = Path(__file__).parent
    followers_path = script_dir / "followers_and_following" / "followers_1.json"
    following_path = script_dir / "followers_and_following" / "following.json"
    output_path = script_dir / "not_following_back.txt"

    # Alternative common naming
    if not followers_path.exists():
        followers_path = script_dir / "followers_and_following" / "followers.json"

    try:
        # Load JSON files
        print(f"\nLoading followers from: {followers_path}")
        followers_data = load_json_file(str(followers_path))

        print(f"Loading following from: {following_path}")
        following_data = load_json_file(str(following_path))

        # Extract usernames
        print("\nExtracting usernames...")
        followers = extract_followers(followers_data)
        following = extract_following(following_data)

        print(f"Found {len(followers)} followers")
        print(f"Found {len(following)} accounts you're following")

        # Find non-followers
        not_following_back = find_non_followers(following, followers)

        # Write results
        if not_following_back:
            write_to_file(not_following_back, str(output_path))
            print(f"\n✓ Found {len(not_following_back)} users who don't follow you back")
            print(f"✓ Results saved to: {output_path}")
        else:
            print("\n✓ Everyone you follow also follows you back!")

    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure you have:")
        print("  1. Requested your Instagram data (Settings → Privacy → Download Your Information)")
        print("  2. Extracted the ZIP file")
        print("  3. Placed the 'followers_and_following' folder in the same directory as this script")

    except json.JSONDecodeError as e:
        print(f"\n✗ Error: Invalid JSON format - {e}")
        print("The JSON files may be corrupted. Try re-downloading your Instagram data.")

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
