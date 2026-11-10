#!/usr/bin/env python3
"""Write the small, fully synthetic sample files of examples/ (used by the tests too). Deterministic."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "examples")


def write(rel, text):
    p = os.path.join(EX, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text.lstrip("\n"))


def main():
    write("dotnet-sample/src/Legacy.Core/Legacy.Core.csproj", """
<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="15.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <PropertyGroup>
    <OutputType>Library</OutputType>
    <TargetFrameworkVersion>v4.7.2</TargetFrameworkVersion>
  </PropertyGroup>
  <ItemGroup>
    <Reference Include="System.Web" />
  </ItemGroup>
</Project>
""")
    write("dotnet-sample/src/Legacy.Core/packages.config", """
<?xml version="1.0" encoding="utf-8"?>
<packages>
  <package id="Newtonsoft.Json" version="12.0.3" targetFramework="net472" />
  <package id="log4net" version="2.0.8" targetFramework="net472" />
</packages>
""")
    write("dotnet-sample/src/Billing.Domain/Billing.Domain.csproj", """
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>netstandard2.0</TargetFramework>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
  </ItemGroup>
</Project>
""")
    write("dotnet-sample/src/Billing.Api/Billing.Api.csproj", """
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
  </PropertyGroup>
  <ItemGroup>
    <ProjectReference Include="..\\Billing.Domain\\Billing.Domain.csproj" />
    <ProjectReference Include="..\\Legacy.Core\\Legacy.Core.csproj" />
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
    <PackageReference Include="Serilog.AspNetCore">
      <Version>8.0.1</Version>
    </PackageReference>
  </ItemGroup>
</Project>
""")
    write("dotnet-sample/tests/Billing.Tests/Billing.Tests.csproj", """
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFrameworks>net8.0;net10.0</TargetFrameworks>
    <OutputType>Exe</OutputType>
  </PropertyGroup>
  <ItemGroup>
    <ProjectReference Include="..\\..\\src\\Billing.Api\\Billing.Api.csproj" />
    <PackageReference Include="xunit" Version="2.9.2" />
    <PackageReference Include="Serilog.AspNetCore" Version="9.0.0" />
  </ItemGroup>
</Project>
""")

    azdo = {"value": [
        {"pullRequestId": 4012, "title": "Round VAT per invoice line", "createdBy": {"displayName": "Camille Martin"},
         "creationDate": "2026-11-03T09:12:44.1234567Z", "isDraft": False, "targetRefName": "refs/heads/main",
         "repository": {"name": "billing"}, "reviewers": [{"displayName": "Hugo Dubois", "vote": 0}]},
        {"pullRequestId": 3550, "title": "Spike: new PDF engine", "createdBy": {"displayName": "Lucas Bernard"},
         "creationDate": "2026-06-20T14:00:00Z", "isDraft": True, "targetRefName": "refs/heads/develop",
         "repository": {"name": "billing"}, "reviewers": []},
        {"pullRequestId": 2101, "title": "Refactor customer search", "createdBy": {"displayName": "Camille Martin"},
         "creationDate": "2025-02-11T08:30:00Z", "isDraft": False, "targetRefName": "refs/heads/develop",
         "repository": {"name": "billing"}, "reviewers": [{"displayName": "Hugo Dubois", "vote": -5},
                                                          {"displayName": "[Billing]\\Reviewers", "vote": 0, "isContainer": True}]},
    ]}
    github = [
        {"number": 88, "title": "fix: decimal comma in CSV import", "author": {"login": "ines-r"}, "createdAt": "2026-10-28T10:00:00Z",
         "updatedAt": "2026-11-09T16:00:00Z", "isDraft": False, "reviewRequests": [{"login": "tom-p"}], "additions": 42, "deletions": 9},
        {"number": 61, "title": "feat: dunning letters", "author": {"login": "tom-p"}, "createdAt": "2026-08-01T10:00:00Z",
         "updatedAt": "2026-08-20T10:00:00Z", "isDraft": False, "reviewRequests": [], "additions": 1840, "deletions": 310},
    ]
    gitlab = [
        {"iid": 17, "title": "Draft: payroll export v2", "author": {"username": "lea.d", "name": "Léa Durand"}, "created_at": "2026-09-14T07:00:00.000Z",
         "updated_at": "2026-09-15T07:00:00.000Z", "draft": True, "reviewers": [], "target_branch": "main", "web_url": "https://gitlab.example.com/x/-/merge_requests/17"},
    ]
    for name, data in (("prs_azure_devops.json", azdo), ("prs_github.json", github), ("prs_gitlab.json", gitlab)):
        write(name, json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print("examples written")


if __name__ == "__main__":
    main()
