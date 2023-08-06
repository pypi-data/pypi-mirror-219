Name: liblnk
Version: 20230716
Release: 1
Summary: Library to access the Windows Shortcut File (LNK) format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/liblnk
               
BuildRequires: gcc               

%description -n liblnk
Library to access the Windows Shortcut File (LNK) format

%package -n liblnk-static
Summary: Library to access the Windows Shortcut File (LNK) format
Group: Development/Libraries
Requires: liblnk = %{version}-%{release}

%description -n liblnk-static
Static library version of liblnk.

%package -n liblnk-devel
Summary: Header files and libraries for developing applications for liblnk
Group: Development/Libraries
Requires: liblnk = %{version}-%{release}

%description -n liblnk-devel
Header files and libraries for developing applications for liblnk.

%package -n liblnk-python3
Summary: Python 3 bindings for liblnk
Group: System Environment/Libraries
Requires: liblnk = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n liblnk-python3
Python 3 bindings for liblnk

%package -n liblnk-tools
Summary: Several tools for reading Windows Shortcut Files (LNK)
Group: Applications/System
Requires: liblnk = %{version}-%{release}

%description -n liblnk-tools
Several tools for reading Windows Shortcut Files (LNK)

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n liblnk
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n liblnk-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n liblnk-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/liblnk.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n liblnk-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n liblnk-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sun Jul 16 2023 Joachim Metz <joachim.metz@gmail.com> 20230716-1
- Auto-generated

