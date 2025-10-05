# typed: false
# frozen_string_literal: true

class IosSimulatorCleaner < Formula
  include Language::Python::Virtualenv

  desc "List and clean iOS simulators and SwiftUI previews"
  homepage "https://github.com/kakashysen/ios-simulator-cleaner"
  url "https://github.com/kakashysen/ios-simulator-cleaner/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "48ed5f4e1e326f8e424c27000b1d51399474faac320d846918cc3ab84760c9a7"
  license "MIT"
  head "https://github.com/kakashysen/ios-simulator-cleaner.git", branch: "main"

  depends_on "python@3.12"

  resource "markdown-it-py" do
    url "https://files.pythonhosted.org/packages/source/m/markdown-it-py/markdown-it-py-3.0.0.tar.gz"
    sha256 "e3f60a94fa066dc52ec76661e37c851cb232d92f9886b15cb560aaada2df8feb"
  end

  resource "mdurl" do
    url "https://files.pythonhosted.org/packages/source/m/mdurl/mdurl-0.1.2.tar.gz"
    sha256 "bb413d29f5eea38f31dd4754dd7377d4465116fb207585f97bf925588687c1ba"
  end

  resource "prompt-toolkit" do
    url "https://files.pythonhosted.org/packages/source/p/prompt_toolkit/prompt_toolkit-3.0.51.tar.gz"
    sha256 "931a162e3b27fc90c86f1b48bb1fb2c528c2761475e57c9c06de13311c7b54ed"
  end

  resource "pygments" do
    url "https://files.pythonhosted.org/packages/source/p/pygments/pygments-2.19.2.tar.gz"
    sha256 "636cb2477cec7f8952536970bc533bc43743542f70392ae026374600add5b887"
  end

  resource "questionary" do
    url "https://files.pythonhosted.org/packages/source/q/questionary/questionary-2.1.0.tar.gz"
    sha256 "6302cdd645b19667d8f6e6634774e9538bfcd1aad9be287e743d96cacaf95587"
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/source/r/rich/rich-14.0.0.tar.gz"
    sha256 "82f1bc23a6a21ebca4ae0c45af9bdbc492ed20231dcb63f297d6d1021a9d5725"
  end

  resource "wcwidth" do
    url "https://files.pythonhosted.org/packages/source/w/wcwidth/wcwidth-0.2.13.tar.gz"
    sha256 "72ea0c06399eb286d978fdedb6923a9eb47e1c486ce63e9b4e64fc18303972b5"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/ios-simulator-cleaner --version")
  end
end
