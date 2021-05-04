from __future__ import division, print_function

import argparse
import os
from lxml import etree

from EuclidWrapper.logging import logger


def defineWrapperProgramOptions():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ecdm_config_xml', type=str, help='The XML config file')
    parser.add_argument('--ecdm_config_xpath', type=str,
                        default="//ConfigurationFile[ModuleName='{}' and count(ParameterName)=0]/FileContainer/FileName",
                        help='The XPath to be used for extracting the Elements config file')
    parser.add_argument('--forward_ecdm_config_xml', type=str,
                        help='The parameter name to forward the ecdm_config_xml to')
    parser.add_argument('--ecdm_extra_config_xpath', type=str,
                        default="//ConfigurationFile[ModuleName='{}' and count(ParameterName)>0]",
                        help='The XPath to be used for extracting additional config files')
    parser.add_argument('--ecdm_extra_config_file_xpath', type=str,
                        default="FileContainer/FileName",
                        help='The XPath to be used for extracting the file name from the extra config files')
    parser.add_argument('--ecdm_extra_config_param_xpath', type=str,
                        default="ParameterName",
                        help='The XPath for extracting the parameter name used to pass the extra config file')
    return parser


def getOptionsToAppend(args, executable):
    options = []

    if args.ecdm_config_xml:
        logger.info('Parsing XML configuration file: {}'.format(args.ecdm_config_xml))

        # Main Elements configuration file
        config_xpath = args.ecdm_config_xpath.replace('{}', executable)
        tree = etree.parse(args.ecdm_config_xml)
        logger.info('Locating Elements config file with XPath: {}'.format(config_xpath))
        config_file = tree.xpath(config_xpath)
        if len(config_file) == 0:
            logger.error('Failed to find the config file element using XPath')
            exit(1)

        if len(config_file) > 1:
            logger.error('XPath query matched multiple main config files')
            exit(1)
        conf_file = os.path.join('data', config_file[0].text.strip())
        logger.info('Found Elements config file: {}'.format(conf_file))
        options.append('--config-file')
        options.append(conf_file)

        if args.forward_ecdm_config_xml:
            options.append('--' + args.forward_ecdm_config_xml)
            options.append(args.ecdm_config_xml)

        # Additional configuration files
        extra_config_xpath = args.ecdm_extra_config_xpath.replace('{}', executable)
        logger.info('Locating additional config files with XPath: {}'.format(extra_config_xpath))
        extra_config_files = tree.xpath(extra_config_xpath)
        for extra_config_file in extra_config_files:
            extra_config_param = extra_config_file.xpath(args.ecdm_extra_config_param_xpath)
            extra_config_filename = extra_config_file.xpath(args.ecdm_extra_config_file_xpath)

            if len(extra_config_param) != 1 or len(extra_config_filename) != 1:
                logger.error('Malformed extra config file: exactly one parameter name and one filename expected')
                exit(1)

            extra_config_param = extra_config_param[0].text.strip()
            extra_config_filename = os.path.join('data', extra_config_filename[0].text.strip())
            logger.info('Found {} = {}'.format(extra_config_param, extra_config_filename))
            options.append('--{}'.format(extra_config_param))
            options.append(extra_config_filename)

    return options

