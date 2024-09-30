### 256 Colors

The following escape codes tells the terminal to use the given color ID:

| PY ESC Code Sequence | Description           |
| :---------------- | :-------------------- |
| `\033[38;5;{ID}m` | Set foreground color. |
| `\033[48;5;{ID}m` | Set background color. |

> Where `{ID}` should be replaced with the color index from 0 to 255 of the following color table:

![256 Color table](color-codes.png)
