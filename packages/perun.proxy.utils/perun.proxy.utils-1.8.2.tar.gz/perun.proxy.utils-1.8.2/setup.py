import setuptools

setuptools.setup(
    name="perun.proxy.utils",
    python_requires=">=3.9",
    url="https://gitlab.ics.muni.cz/perun-proxy-aai/proxyidp-scripts.git",
    description="Module with utilities and monitoring probes",
    include_package_data=True,
    packages=setuptools.find_namespace_packages(include=["perun.*"]),
    install_requires=[
        "setuptools",
        "pymongo~=4.3",
        "asyncssh~=2.13",
        "docker~=6.0",
        "beautifulsoup4~=4.12",
        "requests~=2.31",
        "PyYAML>=5.4,<7.0",
        "check_syncrepl_extended~=2020.13",
        "check_nginx_status~=1.0",
    ],
    extras_require={
        "ldap": [
            "ldap3~=2.9.1",
        ]
    },
    entry_points={
        "console_scripts": [
            "run_probes=perun.proxy.utils.run_probes:main",
            "check_custom_command=perun.proxy.utils.nagios.check_custom_command:main",
            "check_dockers=perun.proxy.utils.nagios.check_dockers:main",
            "check_exabgp_propagation="
            "perun.proxy.utils.nagios.check_exabgp_propagation:main",
            "check_ldap=perun.proxy.utils.nagios.check_ldap:main",
            "check_ldap_syncrepl=check_syncrepl_extended.check_syncrepl_extended:main",
            "check_mongodb=perun.proxy.utils.nagios.check_mongodb:main",
            "check_nginx=check_nginx_status.check_nginx_status:main",
            "check_rpc_status=perun.proxy.utils.nagios.check_rpc_status:main",
            "check_saml=perun.proxy.utils.nagios.check_saml:main",
            "check_user_logins=perun.proxy.utils.nagios.check_user_logins:main",
            "check_webserver_availability="
            "perun.proxy.utils.nagios.webserver_availability:main",
            "metadata_expiration=perun.proxy.utils.metadata_expiration:main",
            "print_docker_versions=perun.proxy.utils.print_docker_versions:main",
            "run_version_script=perun.proxy.utils.run_version_script:main",
            "separate_oidc_logs=perun.proxy.utils.separate_oidc_logs:main",
            "separate_ssp_logs=perun.proxy.utils.separate_ssp_logs:main",
        ]
    },
)
