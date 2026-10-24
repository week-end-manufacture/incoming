class Incoming < Formula
  desc "File organizer and media transcoder"
  homepage "https://github.com/week-end-manufacture/incoming"
  url "https://github.com/week-end-manufacture/incoming/archive/refs/heads/develop.tar.gz"
  version "1.0.0"
  sha256 "08d675d2ae1a0535015eee80d6a9d2f12547406fb6bfa7a5af9dae61b7e993ee"
  license "MIT"

  depends_on "ffmpeg"
  depends_on "handbrake"
  depends_on "imagemagick"
  depends_on "p7zip"

  def install
    cd "src" do
      system "make", "CC=#{ENV.cc}", "CFLAGS=#{ENV.cflags}"
      bin.install "incoming"
    end

    (share/"incoming").install "src/config"
  end

  def caveats
    <<~EOS
      incoming reads its configuration from:
        ~/.config/incoming/settings.json

      Example configuration files were installed to:
        #{share}/incoming/config

      Copy and edit them before the first run:
        mkdir -p ~/.config/incoming
        cp -R #{share}/incoming/config/* ~/.config/incoming/

      Archive support:
        ZIP uses macOS's built-in unzip command.
        7z files require the p7zip formula.
        RAR extraction requires an `unrar` executable installed separately.
    EOS
  end

  test do
    system bin/"incoming", "--version"
  end
end
