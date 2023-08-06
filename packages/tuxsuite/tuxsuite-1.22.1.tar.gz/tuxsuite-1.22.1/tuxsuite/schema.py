# -*- coding: utf-8 -*-

from voluptuous import Any, Optional, Required, Schema, Url, Invalid

SchemaError = Invalid


def plan():
    return Schema(
        {
            Required("version"): 1,
            Optional("name"): str,
            Optional("description"): str,
            Required("jobs"): [
                Any(
                    {Optional("name"): str, Required("build"): dict},
                    {
                        Optional("name"): str,
                        Required("build"): dict,
                        Required("test"): dict,
                    },
                    {
                        Optional("name"): str,
                        Required("build"): dict,
                        Required("tests"): list,
                    },
                    {Optional("name"): str, Required("builds"): list},
                    {
                        Optional("name"): str,
                        Required("builds"): list,
                        Required("test"): dict,
                    },
                    {
                        Optional("name"): str,
                        Required("builds"): list,
                        Required("tests"): list,
                    },
                    {Optional("name"): str, Required("tests"): list},
                    {Optional("name"): str, Required("test"): dict},
                )
            ],
        },
        extra=True,
    )


def bake_plan():
    return Schema(
        {
            Optional("common"): dict,
            Required("version"): 1,
            Optional("name"): str,
            Optional("description"): str,
            Required("jobs"): [
                Any(
                    {Optional("name"): str, Required("bake"): dict},
                    {Optional("name"): str, Required("bakes"): list},
                )
            ],
        },
        extra=True,
    )


def tuxtrigger_config():
    return Schema(
        {
            Required("repositories"): [
                {
                    Optional("branches"): [
                        {
                            Required("name"): str,
                            Required("plan"): str,
                            Optional("squad_project"): str,
                        }
                    ],
                    Required("url"): Url(),
                    Required("squad_group"): str,
                    Optional("regex"): str,
                    Optional("default_plan"): str,
                    Optional("squad_project_prefix"): str,
                }
            ]
        },
        extra=True,
    )
