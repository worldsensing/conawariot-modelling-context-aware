FROM grafana/grafana:8.3.4

ENV HOME /root
ENV GRAFANA_DIR /var/lib/grafana
ENV GRAFANA_PLUGIN_DIR /var/lib/grafana/plugins
ENV GRAFANA_PROVISIONING_DIR /etc/grafana/provisioning
ENV GRAFANA_DASHBOARDS_DIR /etc/grafana/dashboards

USER root
RUN apk update && apk add --no-cache \
    wget unzip

# install plugins
COPY ./config/plugin_list.txt $GRAFANA_PLUGIN_DIR
RUN cd $GRAFANA_PLUGIN_DIR ; while read url ; do wget "${url}" -P . ; unzip ./download ; rm ./download ; done < plugin_list.txt

COPY ./config/datasources.yaml $GRAFANA_PROVISIONING_DIR/datasources/
COPY ./config/dashboards.yaml $GRAFANA_PROVISIONING_DIR/dashboards/

# copy dashboards
RUN mkdir -p $GRAFANA_DASHBOARDS_DIR
COPY ./source/*.json $GRAFANA_DASHBOARDS_DIR/

RUN chown grafana:root $GRAFANA_PLUGIN_DIR -R \
 && chown grafana:root $GRAFANA_PROVISIONING_DIR -R \
 && chown grafana:root $GRAFANA_DASHBOARDS_DIR -R

EXPOSE 3000
USER grafana