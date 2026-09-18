# Arch/CachyOS package definition for the KachyOS security workstation layer.

pkgname=kachysec
pkgver=0.1.0
pkgrel=1
pkgdesc='Modular security workstation control plane for CachyOS'
arch=('any')
url='https://github.com/UseBrainNoL0ve/KachyOS'
license=('MIT')
depends=('python' 'pyside6')
optdepends=('pyside6: optional Qt6 graphical security dashboard')
makedepends=('git' 'python-build' 'python-installer' 'python-setuptools')
source=("git+https://github.com/UseBrainNoL0ve/KachyOS.git#branch=main")
sha256sums=('SKIP')

build() {
    cd "$srcdir/KachyOS"
    python -m build --wheel --no-isolation
}

package() {
    cd "$srcdir/KachyOS"
    python -m installer --destdir="$pkgdir" dist/*.whl
    install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
}
