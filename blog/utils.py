def format_likes(likes):
    if likes >= 1000000:
        return f"{likes/1000000:.1f}M"
    elif likes >= 1000:
        return f"{likes/1000:.1f}K"
    else:
        return str(likes)
