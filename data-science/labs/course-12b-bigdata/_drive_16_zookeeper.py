"""Run 16_zookeeper.sh: a three-server ZooKeeper ensemble on this machine, which needs no Hadoop.

zkCli.sh logs a screenful of INFO lines (its classpath, its environment) on every start; they
are turned down to errors here, through CLIENT_JVMFLAGS, so what each session shows is the
prompt, the command and its answer."""
import pathlib

import hadoop_lab

quiet = pathlib.Path("quiet-logback.xml").resolve()
quiet.write_text('<configuration>\n  <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">\n'
                 '    <encoder><pattern>%msg%n</pattern></encoder>\n  </appender>\n'
                 '  <root level="ERROR"><appender-ref ref="CONSOLE"/></root>\n</configuration>\n')
hadoop_lab.job("16_zookeeper.sh", [], then_file=True, hadoop=False,
               extra_env={"CLIENT_JVMFLAGS": f"-Dlogback.configurationFile={quiet}"})
